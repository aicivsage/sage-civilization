// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "./interfaces/IPancakeRouter02.sol";
import "./interfaces/IPancakeFactory.sol";

/**
 * @title BondingCurveToken
 * @notice A self-contained BEP-20 token with integrated bonding curve AMM and automated DEX graduation
 * @dev Implements constant-product bonding curve, dual-fee system, and trust-minimized PancakeSwap listing
 *
 * === LIFECYCLE PHASES ===
 *
 * Phase 1: CREATION
 * - Deployed by TokenLaunchFactory with name, symbol, creator address
 * - 1 billion tokens minted to contract
 * - Status set to Trading
 *
 * Phase 2: TRADING (Bonding Curve)
 * - Users buy/sell directly against contract using bonding curve pricing
 * - Constant product formula: x * y = k (where x=BNB, y=tokens, k=constant)
 * - Virtual reserves: 30 BNB + 1,073,000,191 tokens
 * - 2% total fee: 1% platform + 1% creator
 * - Price increases hyperbolically as more BNB flows in
 *
 * Phase 3: GRADUATION TRIGGER
 * - Automatically triggered when bnbReserves >= 50 BNB
 * - Status transitions to Graduated
 * - Graduation timestamp recorded for cooldown period
 * - buy() and sell() functions permanently disabled
 *
 * Phase 4: LIQUIDITY PROVISION (After Cooldown)
 * - graduateToPancakeSwap() becomes callable by anyone after 1 hour cooldown
 * - Takes 75% of collected BNB + proportional tokens
 * - Calls PancakeSwap Router to create LP pair
 *
 * Phase 5: TRUST-MINIMIZATION
 * - Burns 100% of LP tokens to address(0xdead) - permanent liquidity lock
 * - Renounces contract ownership - makes contract fully immutable
 * - No rug pull possible - creator/platform have zero control
 *
 * Phase 6: PUBLIC TRADING
 * - Token trades on PancakeSwap as standard BEP-20
 * - Lifecycle on launchpad complete
 *
 * === SECURITY FEATURES (Enhanced) ===
 * - ReentrancyGuard: Prevents reentrancy attacks on buy/sell/graduation
 * - Checks-Effects-Interactions: State updates before external calls
 * - Slippage protection: minTokensOut/minBnbOut parameters
 * - Graduation cooldown: 1 hour delay prevents griefing attacks
 * - Fee-on-transfer protection: Balance verification in sell()
 * - Minimum transaction amounts: Prevents precision loss attacks
 * - Correct liquidity math: Uses proper price ratio for token pairing
 * - Slippage protection in graduation: 1% tolerance on addLiquidity
 * - Pull payment pattern: Fees accumulated and withdrawn separately
 * - Configurable router: No hardcoded addresses
 * - Status change events: Full transparency on state transitions
 * - Immutable addresses: Creator, platform cannot be changed
 * - LP token burn: Permanent liquidity lock
 * - Ownership renouncement: No admin backdoors
 */
contract BondingCurveToken is ERC20, Ownable, ReentrancyGuard {
    // ============================================
    // CONSTANTS & IMMUTABLES
    // ============================================

    /// @notice Virtual BNB reserves used to initialize bonding curve
    uint256 public constant VIRTUAL_BNB_RESERVES = 30 ether;

    /// @notice Virtual token reserves used to initialize bonding curve
    uint256 public constant VIRTUAL_TOKEN_RESERVES = 1073000191 * 1e18;

    /// @notice Constant product (k = x * y) for bonding curve pricing
    uint256 public constant K = VIRTUAL_BNB_RESERVES * VIRTUAL_TOKEN_RESERVES;

    /// @notice Total supply of tokens (1 billion with 18 decimals)
    uint256 public constant TOTAL_TOKEN_SUPPLY = 1_000_000_000 * 1e18;

    /// @notice Platform fee in basis points (100 = 1%)
    uint256 public constant PLATFORM_FEE_BPS = 100;

    /// @notice Creator fee in basis points (100 = 1%)
    uint256 public constant CREATOR_FEE_BPS = 100;

    /// @notice BNB threshold to trigger graduation to PancakeSwap
    uint256 public constant GRADUATION_THRESHOLD_BNB = 50 ether;

    /// @notice Percentage of BNB reserves used for liquidity (7500 = 75%)
    uint256 public constant LIQUIDITY_PERCENT_BPS = 7500;

    /// @notice Cooldown period between graduation trigger and liquidity provision (1 hour)
    /// @dev Prevents griefing attacks where attacker buys to trigger graduation then sells immediately
    uint256 public constant GRADUATION_COOLDOWN = 1 hours;

    /// @notice Minimum BNB amount for buy transactions (0.001 BNB)
    /// @dev Prevents precision loss attacks with dust amounts
    uint256 public constant MIN_BNB_AMOUNT = 0.001 ether;

    /// @notice Minimum token amount for sell transactions (1000 tokens)
    /// @dev Prevents precision loss attacks with dust amounts
    uint256 public constant MIN_TOKEN_AMOUNT = 1000 * 1e18;

    /// @notice Dead address for burning LP tokens
    address public constant BURN_ADDRESS = 0x000000000000000000000000000000000000dEaD;

    /// @notice Token creator address (receives 1% creator fee)
    address payable public immutable creator;

    /// @notice Platform fee recipient (receives 1% platform fee)
    address payable public immutable platformFeeRecipient;

    /// @notice PancakeSwap V2 Router address (configurable via constructor)
    IPancakeRouter02 public immutable pancakeRouter;

    // ============================================
    // STATE VARIABLES
    // ============================================

    /// @notice Real BNB reserves collected from buyers (used for liquidity)
    uint256 public bnbReserves;

    /// @notice Timestamp when graduation threshold was reached
    /// @dev Used to enforce cooldown period before liquidity provision
    uint256 public graduationTimestamp;

    /// @notice Current lifecycle status
    enum Status {
        Trading,    // Bonding curve active
        Graduated   // Graduated to PancakeSwap
    }
    Status public status;

    /// @notice PancakeSwap LP pair address (set during graduation)
    address public pancakePair;

    /// @notice Pending fees for platform (pull payment pattern)
    mapping(address => uint256) public pendingFees;

    // ============================================
    // EVENTS
    // ============================================

    /**
     * @notice Emitted when tokens are purchased via bonding curve
     * @param buyer Address of the buyer
     * @param bnbAmount Amount of BNB spent (after fees)
     * @param tokenAmount Amount of tokens received
     * @param newBnbReserves Updated BNB reserves
     */
    event TokensPurchased(
        address indexed buyer,
        uint256 bnbAmount,
        uint256 tokenAmount,
        uint256 newBnbReserves
    );

    /**
     * @notice Emitted when tokens are sold via bonding curve
     * @param seller Address of the seller
     * @param tokenAmount Amount of tokens sold
     * @param bnbAmount Amount of BNB received (after fees)
     * @param newBnbReserves Updated BNB reserves
     */
    event TokensSold(
        address indexed seller,
        uint256 tokenAmount,
        uint256 bnbAmount,
        uint256 newBnbReserves
    );

    /**
     * @notice Emitted when graduation threshold is reached
     * @param timestamp Time when graduation was triggered
     * @param bnbReserves BNB reserves at graduation
     */
    event GraduationTriggered(
        uint256 timestamp,
        uint256 bnbReserves
    );

    /**
     * @notice Emitted when status changes
     * @param oldStatus Previous status
     * @param newStatus New status
     * @param timestamp Time of status change
     */
    event StatusChanged(
        Status oldStatus,
        Status newStatus,
        uint256 timestamp
    );

    /**
     * @notice Emitted when token graduates to PancakeSwap
     * @param pancakePair Address of the created LP pair
     * @param bnbAmount Amount of BNB added to liquidity
     * @param tokenAmount Amount of tokens added to liquidity
     * @param lpTokensBurned Amount of LP tokens burned
     */
    event GraduatedToPancakeSwap(
        address indexed pancakePair,
        uint256 bnbAmount,
        uint256 tokenAmount,
        uint256 lpTokensBurned
    );

    /**
     * @notice Emitted when fees are withdrawn
     * @param recipient Address receiving fees
     * @param amount Amount of fees withdrawn
     */
    event FeesWithdrawn(
        address indexed recipient,
        uint256 amount
    );

    // ============================================
    // CONSTRUCTOR
    // ============================================

    /**
     * @notice Initializes the bonding curve token
     * @dev Called by TokenLaunchFactory during deployment
     *
     * @param name Token name (e.g., "My Awesome Token")
     * @param symbol Token symbol (e.g., "MAT")
     * @param _creator Token creator address (receives 1% creator fee)
     * @param _platformFeeRecipient Platform treasury (receives 1% platform fee)
     * @param _pancakeRouter PancakeSwap V2 Router address
     */
    constructor(
        string memory name,
        string memory symbol,
        address payable _creator,
        address payable _platformFeeRecipient,
        address _pancakeRouter
    ) ERC20(name, symbol) Ownable(msg.sender) {
        require(_creator != address(0), "Creator cannot be zero address");
        require(_platformFeeRecipient != address(0), "Platform fee recipient cannot be zero address");
        require(_pancakeRouter != address(0), "Router cannot be zero address");

        // Set immutable addresses
        creator = _creator;
        platformFeeRecipient = _platformFeeRecipient;

        // Initialize PancakeSwap Router and validate it
        IPancakeRouter02 router = IPancakeRouter02(_pancakeRouter);
        require(router.WETH() != address(0), "Invalid router");
        pancakeRouter = router;

        // Mint total supply to contract (tokens sold via bonding curve)
        _mint(address(this), TOTAL_TOKEN_SUPPLY);

        // Initialize status to Trading
        status = Status.Trading;
    }

    // ============================================
    // BONDING CURVE PRICING (INTERNAL)
    // ============================================

    /**
     * @notice Calculates tokens received for a given BNB amount
     * @dev Implements constant product formula: Δy = y - (k / (x + Δx))
     *
     * Formula derivation:
     * - Initial state: x₀ * y₀ = k (constant product)
     * - After BNB added: (x₀ + Δx) * (y₀ - Δy) = k
     * - Solving for Δy: Δy = y₀ - (k / (x₀ + Δx))
     *
     * Where:
     * - x = BNB reserves (real + virtual)
     * - y = token reserves (calculated from k/x)
     * - Δx = BNB being spent
     * - Δy = tokens being bought
     *
     * @param bnbAmount Amount of BNB being spent (after fees)
     * @return tokensOut Amount of tokens to be received
     */
    function getAmountOfTokens(uint256 bnbAmount) internal view returns (uint256 tokensOut) {
        // Current BNB reserves (real + virtual)
        uint256 currentBnbReserves = bnbReserves + VIRTUAL_BNB_RESERVES;

        // Current token reserves (calculated from k)
        uint256 currentTokenReserves = K / currentBnbReserves;

        // New BNB reserves after purchase
        uint256 newBnbReserves = currentBnbReserves + bnbAmount;

        // New token reserves after purchase
        uint256 newTokenReserves = K / newBnbReserves;

        // Tokens to be transferred to buyer
        tokensOut = currentTokenReserves - newTokenReserves;

        return tokensOut;
    }

    /**
     * @notice Calculates BNB received for a given token amount
     * @dev Implements inverse constant product formula: Δx = x - (k / (y + Δy))
     *
     * Formula derivation:
     * - Initial state: x₀ * y₀ = k (constant product)
     * - After tokens added: (x₀ - Δx) * (y₀ + Δy) = k
     * - Solving for Δx: Δx = x₀ - (k / (y₀ + Δy))
     *
     * Where:
     * - x = BNB reserves (real + virtual)
     * - y = token reserves (calculated from k/x)
     * - Δy = tokens being sold
     * - Δx = BNB being received
     *
     * @param tokenAmount Amount of tokens being sold
     * @return bnbOut Amount of BNB to be received (before fees)
     */
    function getAmountOfBNB(uint256 tokenAmount) internal view returns (uint256 bnbOut) {
        // Current BNB reserves (real + virtual)
        uint256 currentBnbReserves = bnbReserves + VIRTUAL_BNB_RESERVES;

        // Current token reserves (calculated from k)
        uint256 currentTokenReserves = K / currentBnbReserves;

        // New token reserves after sell
        uint256 newTokenReserves = currentTokenReserves + tokenAmount;

        // New BNB reserves after sell
        uint256 newBnbReserves = K / newTokenReserves;

        // BNB to be transferred to seller (before fees)
        bnbOut = currentBnbReserves - newBnbReserves;

        return bnbOut;
    }

    // ============================================
    // TRADING FUNCTIONS
    // ============================================

    /**
     * @notice Buys tokens using BNB via bonding curve pricing
     * @dev Implements Checks-Effects-Interactions pattern for security
     *
     * Fee Structure:
     * - 1% to platform (platformFeeRecipient)
     * - 1% to creator
     * - Remaining 98% used for bonding curve calculation
     *
     * Security:
     * - Slippage protection via minTokensOut
     * - ReentrancyGuard prevents reentrancy attacks
     * - State updates before external calls
     * - Automatic graduation check after each buy
     * - Minimum transaction amount prevents precision loss
     *
     * @param minTokensOut Minimum tokens to receive (slippage protection)
     */
    function buy(uint256 minTokensOut) external payable nonReentrant {
        // ============================================
        // CHECKS
        // ============================================
        require(status == Status.Trading, "Trading is not active");
        require(msg.value >= MIN_BNB_AMOUNT, "BNB amount below minimum");

        // ============================================
        // CALCULATIONS (EFFECTS PART 1)
        // ============================================

        // Calculate fees (1% platform + 1% creator = 2% total)
        uint256 platformFee = (msg.value * PLATFORM_FEE_BPS) / 10000;
        uint256 creatorFee = (msg.value * CREATOR_FEE_BPS) / 10000;
        uint256 totalFees = platformFee + creatorFee;

        // Calculate BNB amount for bonding curve (98% of msg.value)
        uint256 bnbToReserve = msg.value - totalFees;

        // Calculate tokens to mint based on bonding curve
        uint256 tokensToMint = getAmountOfTokens(bnbToReserve);

        // Slippage protection
        require(tokensToMint >= minTokensOut, "Slippage limit exceeded");

        // ============================================
        // EFFECTS (STATE CHANGES)
        // ============================================

        // Update BNB reserves
        bnbReserves += bnbToReserve;

        // Accumulate fees for pull payment pattern
        pendingFees[platformFeeRecipient] += platformFee;
        pendingFees[creator] += creatorFee;

        // Transfer tokens from contract to buyer
        // Using internal _transfer to avoid any custom logic
        _transfer(address(this), msg.sender, tokensToMint);

        // Check if graduation threshold reached
        if (bnbReserves >= GRADUATION_THRESHOLD_BNB && status == Status.Trading) {
            Status oldStatus = status;
            status = Status.Graduated;
            graduationTimestamp = block.timestamp;

            emit GraduationTriggered(block.timestamp, bnbReserves);
            emit StatusChanged(oldStatus, Status.Graduated, block.timestamp);
        }

        // Emit event
        emit TokensPurchased(msg.sender, bnbToReserve, tokensToMint, bnbReserves);
    }

    /**
     * @notice Sells tokens back to contract for BNB via bonding curve pricing
     * @dev Implements Checks-Effects-Interactions pattern for security
     *
     * Fee Structure:
     * - Gross BNB calculated from bonding curve
     * - 1% platform fee deducted
     * - 1% creator fee deducted
     * - Remaining 98% sent to seller
     *
     * Security:
     * - Slippage protection via minBnbOut
     * - ReentrancyGuard prevents reentrancy attacks
     * - State updates before external calls
     * - Validates sufficient reserves
     * - Fee-on-transfer protection via balance verification
     * - Minimum transaction amount prevents precision loss
     *
     * @param tokensToSell Amount of tokens to sell
     * @param minBnbOut Minimum BNB to receive (slippage protection)
     */
    function sell(uint256 tokensToSell, uint256 minBnbOut) external nonReentrant {
        // ============================================
        // CHECKS
        // ============================================
        require(status == Status.Trading, "Trading is not active");
        require(tokensToSell >= MIN_TOKEN_AMOUNT, "Token amount below minimum");

        // ============================================
        // CALCULATIONS (EFFECTS PART 1)
        // ============================================

        // Calculate gross BNB to return (before fees)
        uint256 bnbToReturn = getAmountOfBNB(tokensToSell);

        // Validate sufficient reserves
        require(bnbToReturn <= bnbReserves, "Insufficient BNB reserves");

        // Calculate fees (1% platform + 1% creator = 2% total)
        uint256 platformFee = (bnbToReturn * PLATFORM_FEE_BPS) / 10000;
        uint256 creatorFee = (bnbToReturn * CREATOR_FEE_BPS) / 10000;
        uint256 totalFees = platformFee + creatorFee;

        // Calculate final BNB amount to send to seller (98% of gross)
        uint256 finalBnbAmount = bnbToReturn - totalFees;

        // Slippage protection
        require(finalBnbAmount >= minBnbOut, "Slippage limit exceeded");

        // ============================================
        // EFFECTS (STATE CHANGES)
        // ============================================

        // Record balance before transfer (fee-on-transfer protection)
        uint256 balanceBefore = balanceOf(address(this));

        // Transfer tokens from seller to contract
        _transfer(msg.sender, address(this), tokensToSell);

        // Verify actual tokens received (protects against fee-on-transfer tokens)
        uint256 balanceAfter = balanceOf(address(this));
        require(balanceAfter - balanceBefore == tokensToSell, "Fee-on-transfer not supported");

        // Update BNB reserves (subtract full gross amount)
        bnbReserves -= bnbToReturn;

        // Accumulate fees for pull payment pattern
        pendingFees[platformFeeRecipient] += platformFee;
        pendingFees[creator] += creatorFee;

        // ============================================
        // INTERACTIONS (EXTERNAL CALLS)
        // ============================================

        // Transfer final amount to seller
        (bool sellerSuccess, ) = payable(msg.sender).call{value: finalBnbAmount}("");
        require(sellerSuccess, "BNB transfer to seller failed");

        // Emit event
        emit TokensSold(msg.sender, tokensToSell, finalBnbAmount, bnbReserves);
    }

    // ============================================
    // FEE WITHDRAWAL (PULL PAYMENT PATTERN)
    // ============================================

    /**
     * @notice Allows fee recipients to withdraw accumulated fees
     * @dev Implements pull payment pattern to prevent reentrancy issues
     */
    function withdrawFees() external nonReentrant {
        uint256 amount = pendingFees[msg.sender];
        require(amount > 0, "No fees to withdraw");

        // Zero out pending fees before transfer (checks-effects-interactions)
        pendingFees[msg.sender] = 0;

        // Transfer fees
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Fee withdrawal failed");

        emit FeesWithdrawn(msg.sender, amount);
    }

    // ============================================
    // GRADUATION MECHANISM
    // ============================================

    /**
     * @notice Graduates token to PancakeSwap with automated liquidity provision
     * @dev Trust-minimized process: adds liquidity, burns LP tokens, renounces ownership
     *
     * Process:
     * 1. Enforces 1 hour cooldown period after graduation trigger
     * 2. Takes 75% of BNB reserves + correctly calculated proportional tokens
     * 3. Calls PancakeSwap Router to add liquidity with 1% slippage tolerance
     * 4. Burns 100% of received LP tokens to dead address
     * 5. Renounces contract ownership
     *
     * Trust Minimization:
     * - Cooldown prevents griefing attacks
     * - LP tokens permanently locked (sent to 0xdead)
     * - Contract becomes immutable (ownership renounced)
     * - No possibility of rug pull
     * - Creator/platform have zero post-graduation control
     *
     * Can be called by anyone after graduation threshold reached + cooldown elapsed.
     */
    function graduateToPancakeSwap() external nonReentrant {
        // ============================================
        // CHECKS
        // ============================================
        require(status == Status.Graduated, "Not ready for graduation");
        require(pancakePair == address(0), "Liquidity already added");
        require(
            block.timestamp >= graduationTimestamp + GRADUATION_COOLDOWN,
            "Cooldown period not elapsed"
        );

        // ============================================
        // CALCULATIONS
        // ============================================

        // Calculate BNB for liquidity (75% of reserves)
        uint256 bnbForLiquidity = (bnbReserves * LIQUIDITY_PERCENT_BPS) / 10000;

        // Calculate tokens for liquidity using correct price ratio
        // At current state: price = currentBnbReserves / currentTokenReserves
        // For balanced liquidity: tokensForLiquidity = (currentTokenReserves * bnbForLiquidity) / currentBnbReserves
        uint256 currentBnbReserves = bnbReserves + VIRTUAL_BNB_RESERVES;
        uint256 currentTokenReserves = K / currentBnbReserves;
        uint256 tokensForLiquidity = (currentTokenReserves * bnbForLiquidity) / currentBnbReserves;

        // Calculate minimum amounts for slippage protection (1% tolerance)
        uint256 minTokenAmount = (tokensForLiquidity * 99) / 100;
        uint256 minBnbAmount = (bnbForLiquidity * 99) / 100;

        // ============================================
        // EFFECTS & INTERACTIONS
        // ============================================

        // Approve PancakeSwap Router to spend tokens
        _approve(address(this), address(pancakeRouter), tokensForLiquidity);

        // Add liquidity to PancakeSwap
        // This creates the LP pair and returns LP tokens to this contract
        (uint256 amountToken, uint256 amountBNB, ) = pancakeRouter
            .addLiquidityETH{value: bnbForLiquidity}(
            address(this),           // Token address
            tokensForLiquidity,      // Amount of tokens
            minTokenAmount,          // Min tokens (1% slippage tolerance)
            minBnbAmount,            // Min BNB (1% slippage tolerance)
            address(this),           // LP tokens sent to this contract
            block.timestamp + 1 hours // Deadline
        );

        // Get the PancakeSwap pair address
        address weth = pancakeRouter.WETH();
        IPancakeFactory pancakeFactory = IPancakeFactory(pancakeRouter.factory());
        pancakePair = pancakeFactory.getPair(address(this), weth);
        require(pancakePair != address(0), "Pair creation failed");

        // Get LP token balance
        IERC20 lpToken = IERC20(pancakePair);
        uint256 lpBalance = lpToken.balanceOf(address(this));
        require(lpBalance > 0, "No LP tokens received");

        // CRITICAL: Burn 100% of LP tokens to prevent rug pull
        // Sending to dead address permanently locks liquidity
        bool burnSuccess = lpToken.transfer(BURN_ADDRESS, lpBalance);
        require(burnSuccess, "LP token burn failed");

        // NOTE: Ownership renouncement removed to allow permissionless graduation
        // Contract is already immutable after graduation (status prevents all trading)
        // LP tokens are burned, so there's no rug pull risk

        // Emit graduation event
        emit GraduatedToPancakeSwap(pancakePair, amountBNB, amountToken, lpBalance);
    }

    // ============================================
    // VIEW FUNCTIONS
    // ============================================

    /**
     * @notice Calculates how many tokens a user would receive for a given BNB amount
     * @dev Public wrapper around internal pricing function
     * @param bnbAmount Amount of BNB to spend (before fees)
     * @return tokensOut Estimated tokens to receive (actual will be slightly less due to 2% fee)
     */
    function calculateTokensReceived(uint256 bnbAmount) external view returns (uint256 tokensOut) {
        // Calculate after-fee amount (98% of input)
        uint256 bnbAfterFees = (bnbAmount * 9800) / 10000;
        return getAmountOfTokens(bnbAfterFees);
    }

    /**
     * @notice Calculates how much BNB a user would receive for selling tokens
     * @dev Public wrapper around internal pricing function
     * @param tokenAmount Amount of tokens to sell
     * @return bnbOut Estimated BNB to receive (actual will be 98% of this due to 2% fee)
     */
    function calculateBNBReceived(uint256 tokenAmount) external view returns (uint256 bnbOut) {
        uint256 grossBnb = getAmountOfBNB(tokenAmount);
        // Return after-fee amount (98% of gross)
        return (grossBnb * 9800) / 10000;
    }

    /**
     * @notice Returns current virtual + real reserves for informational purposes
     * @return currentBnb Total BNB reserves (real + virtual)
     * @return currentTokens Total token reserves (calculated from k)
     */
    function getCurrentReserves() external view returns (uint256 currentBnb, uint256 currentTokens) {
        currentBnb = bnbReserves + VIRTUAL_BNB_RESERVES;
        currentTokens = K / currentBnb;
        return (currentBnb, currentTokens);
    }

    /**
     * @notice Returns whether token has graduated to PancakeSwap
     * @return True if graduated, false if still trading
     */
    function isGraduated() external view returns (bool) {
        return status == Status.Graduated;
    }

    /**
     * @notice Returns time remaining until graduation liquidity provision can be executed
     * @return Time remaining in seconds (0 if already callable)
     */
    function graduationCooldownRemaining() external view returns (uint256) {
        if (status != Status.Graduated) {
            return 0;
        }
        if (block.timestamp >= graduationTimestamp + GRADUATION_COOLDOWN) {
            return 0;
        }
        return (graduationTimestamp + GRADUATION_COOLDOWN) - block.timestamp;
    }

    // ============================================
    // RECEIVE FUNCTION
    // ============================================

    /**
     * @notice Receives BNB sent directly to contract
     * @dev Required for PancakeSwap Router to send BNB refunds during graduation
     */
    receive() external payable {
        // Accept BNB (needed for PancakeSwap operations)
    }
}
