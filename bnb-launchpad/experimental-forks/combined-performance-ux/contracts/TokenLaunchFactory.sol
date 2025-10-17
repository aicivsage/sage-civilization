// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./BondingCurveToken.sol";

/**
 * @title TokenLaunchFactory
 * @notice Factory contract for permissionless token creation with bonding curve mechanics
 * @dev Implements the Factory pattern for secure, isolated token deployments
 *
 * This contract serves as the central entry point for creating new tokens on the launchpad.
 * Each token is deployed as an independent BondingCurveToken contract instance, ensuring
 * complete isolation of logic, state, and funds. An exploit in one token cannot affect
 * any other token launched through this factory.
 *
 * Architecture Benefits:
 * - Security: Complete compartmentalization at the contract address level
 * - Scalability: Unlimited token deployments without state bloat
 * - Maintainability: Clear separation of concerns between factory and token logic
 * - Trust-minimization: Each token is independently verifiable
 *
 * The factory is owned (initially by deployer, should be transferred to multisig/DAO)
 * to allow platform-level parameter updates without compromising token immutability.
 *
 * Security Enhancement:
 * - Configurable PancakeSwap Router address (no hardcoded addresses)
 * - Router validation during factory deployment
 * - Router address passed to each token deployment
 */
contract TokenLaunchFactory is Ownable {
    // ============================================
    // STATE VARIABLES
    // ============================================

    /**
     * @notice Platform treasury address that receives 1% fee from all trades
     * @dev Immutable to prevent unauthorized changes and save gas on reads
     */
    address payable public immutable platformFeeRecipient;

    /**
     * @notice PancakeSwap V2 Router address (configurable, not hardcoded)
     * @dev Immutable to save gas on reads, validated during deployment
     */
    IPancakeRouter02 public immutable pancakeRouter;

    /**
     * @notice Array of all token addresses deployed by this factory
     * @dev Provides on-chain enumeration of launched tokens
     */
    address[] public allTokens;

    // ============================================
    // EVENTS
    // ============================================

    /**
     * @notice Emitted when a new token is successfully created
     * @dev Indexed parameters enable efficient off-chain filtering and discovery
     *
     * @param tokenAddress Address of the newly deployed BondingCurveToken contract
     * @param creator Address of the user who created the token
     * @param name Full name of the token
     * @param symbol Ticker symbol of the token
     */
    event TokenCreated(
        address indexed tokenAddress,
        address indexed creator,
        string name,
        string symbol
    );

    // ============================================
    // CONSTRUCTOR
    // ============================================

    /**
     * @notice Initializes the factory with platform fee recipient and PancakeSwap router
     * @dev Validates both addresses before deployment
     *
     * @param _platformFeeRecipient Address to receive platform fees (must not be zero address)
     * @param _pancakeRouter PancakeSwap V2 Router address (must be valid router contract)
     */
    constructor(
        address payable _platformFeeRecipient,
        address _pancakeRouter
    ) Ownable(msg.sender) {
        require(_platformFeeRecipient != address(0), "Platform fee recipient cannot be zero address");
        require(_pancakeRouter != address(0), "Router cannot be zero address");

        // Validate router by checking WETH address
        IPancakeRouter02 router = IPancakeRouter02(_pancakeRouter);
        require(router.WETH() != address(0), "Invalid router");

        platformFeeRecipient = _platformFeeRecipient;
        pancakeRouter = router;
    }

    // ============================================
    // EXTERNAL FUNCTIONS
    // ============================================

    /**
     * @notice Creates a new token with bonding curve mechanics
     * @dev Permissionless function - anyone can create a token
     *
     * This function deploys a new BondingCurveToken instance with:
     * - Bonding curve pricing (constant product AMM simulation)
     * - 1 billion token total supply
     * - Dual fee structure (1% platform + 1% creator)
     * - Automated graduation to PancakeSwap at 50 BNB threshold
     * - Trust-minimized LP token burn and ownership renouncement
     * - Configurable PancakeSwap router (passed from factory)
     *
     * @param name Full name for the token (e.g., "My Awesome Token")
     * @param symbol Ticker symbol for the token (e.g., "MAT")
     * @return tokenAddress Address of the newly deployed token contract
     */
    function createToken(
        string memory name,
        string memory symbol
    ) external returns (address tokenAddress) {
        // Deploy new BondingCurveToken instance with router address
        // msg.sender becomes the token creator (receives 1% creator fee)
        BondingCurveToken newToken = new BondingCurveToken(
            name,
            symbol,
            payable(msg.sender),         // Token creator address
            platformFeeRecipient,         // Platform fee recipient address
            address(pancakeRouter)        // PancakeSwap Router address
        );

        // Get the deployed contract address
        tokenAddress = address(newToken);

        // Add to registry for enumeration
        allTokens.push(tokenAddress);

        // Emit event for off-chain indexing
        emit TokenCreated(tokenAddress, msg.sender, name, symbol);

        return tokenAddress;
    }

    /**
     * @notice Returns all token addresses deployed by this factory
     * @dev Useful for off-chain services to enumerate all launched tokens
     * @return Array of all token contract addresses
     */
    function getAllTokens() external view returns (address[] memory) {
        return allTokens;
    }

    /**
     * @notice Returns the total number of tokens created
     * @return Total count of deployed tokens
     */
    function getTokenCount() external view returns (uint256) {
        return allTokens.length;
    }
}
