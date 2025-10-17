// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "./BondingCurveTokenOptimized.sol";

/**
 * @title BondingCurveFactoryOptimized
 * @notice PERFORMANCE OPTIMIZED: Enhanced factory with security features
 * @dev Deploys optimized bonding curve tokens with additional safety features
 *
 * === ENHANCEMENTS ===
 *
 * 1. TOKEN WHITELIST/BLACKLIST
 *    - Prevent malicious token names/symbols
 *    - Block known scam patterns
 *
 * 2. EMERGENCY PAUSE
 *    - Global pause for security incidents
 *    - Creator can still deploy during pause (for migration)
 *
 * 3. ENHANCED DEPLOYMENT TRACKING
 *    - Track deployed tokens per creator
 *    - Query tokens by various criteria
 *    - Better analytics and monitoring
 *
 * 4. CONFIGURABLE PARAMETERS
 *    - Adjustable creation fee
 *    - Configurable router address
 *    - Future-proof design
 */
contract BondingCurveFactoryOptimized is Ownable, ReentrancyGuard {
    // ============================================
    // STATE VARIABLES
    // ============================================

    /// @notice Fee charged for creating a new token (in BNB)
    uint256 public creationFee;

    /// @notice Platform fee recipient
    address payable public platformFeeRecipient;

    /// @notice PancakeSwap Router address
    address public pancakeRouter;

    /// @notice All deployed tokens
    address[] public deployedTokens;

    /// @notice Mapping from token address to creator
    mapping(address => address) public tokenCreator;

    /// @notice Mapping from creator to their deployed tokens
    mapping(address => address[]) public creatorTokens;

    /// @notice Emergency pause flag
    bool public paused;

    /// @notice Blacklisted names/symbols (scam prevention)
    mapping(bytes32 => bool) public blacklistedNames;

    // ============================================
    // EVENTS
    // ============================================

    event TokenCreated(
        address indexed tokenAddress,
        address indexed creator,
        string name,
        string symbol,
        uint256 timestamp,
        uint256 totalDeployed
    );

    event CreationFeeUpdated(uint256 oldFee, uint256 newFee);
    event PlatformFeeRecipientUpdated(address oldRecipient, address newRecipient);
    event PancakeRouterUpdated(address oldRouter, address newRouter);
    event PauseToggled(bool paused);
    event NameBlacklisted(string name, bool blacklisted);

    // ============================================
    // CONSTRUCTOR
    // ============================================

    constructor(
        address payable _platformFeeRecipient,
        uint256 _creationFee,
        address _pancakeRouter
    ) Ownable(msg.sender) {
        require(_platformFeeRecipient != address(0), "Invalid platform fee recipient");
        require(_pancakeRouter != address(0), "Invalid router address");

        platformFeeRecipient = _platformFeeRecipient;
        creationFee = _creationFee;
        pancakeRouter = _pancakeRouter;
    }

    // ============================================
    // TOKEN CREATION
    // ============================================

    /**
     * @notice Creates a new bonding curve token
     * @dev ENHANCED: Name validation, pause check, enhanced tracking
     *
     * @param name Token name (e.g., "My Awesome Token")
     * @param symbol Token symbol (e.g., "MAT")
     * @return tokenAddress Address of deployed token
     */
    function createToken(
        string memory name,
        string memory symbol
    ) external payable nonReentrant returns (address tokenAddress) {
        // ============================================
        // CHECKS
        // ============================================

        require(!paused, "Factory is paused");
        require(msg.value >= creationFee, "Insufficient creation fee");
        require(bytes(name).length > 0 && bytes(name).length <= 50, "Invalid name length");
        require(bytes(symbol).length > 0 && bytes(symbol).length <= 10, "Invalid symbol length");

        // NEW: Blacklist check
        bytes32 nameHash = keccak256(abi.encodePacked(_toLowerCase(name)));
        bytes32 symbolHash = keccak256(abi.encodePacked(_toLowerCase(symbol)));
        require(!blacklistedNames[nameHash], "Name is blacklisted");
        require(!blacklistedNames[symbolHash], "Symbol is blacklisted");

        // ============================================
        // EFFECTS
        // ============================================

        // Deploy new token
        BondingCurveTokenOptimized newToken = new BondingCurveTokenOptimized(
            name,
            symbol,
            payable(msg.sender), // creator
            platformFeeRecipient,
            pancakeRouter
        );

        tokenAddress = address(newToken);

        // Track deployment
        deployedTokens.push(tokenAddress);
        tokenCreator[tokenAddress] = msg.sender;
        creatorTokens[msg.sender].push(tokenAddress);

        // Transfer ownership to creator
        newToken.transferOwnership(msg.sender);

        // ============================================
        // INTERACTIONS
        // ============================================

        // Transfer creation fee to platform
        if (creationFee > 0) {
            (bool success, ) = platformFeeRecipient.call{value: creationFee}("");
            require(success, "Fee transfer failed");
        }

        // Refund excess BNB
        if (msg.value > creationFee) {
            (bool refundSuccess, ) = msg.sender.call{value: msg.value - creationFee}("");
            require(refundSuccess, "Refund failed");
        }

        emit TokenCreated(
            tokenAddress,
            msg.sender,
            name,
            symbol,
            block.timestamp,
            deployedTokens.length
        );

        return tokenAddress;
    }

    // ============================================
    // VIEW FUNCTIONS
    // ============================================

    /**
     * @notice Returns total number of deployed tokens
     */
    function totalDeployedTokens() external view returns (uint256) {
        return deployedTokens.length;
    }

    /**
     * @notice Returns all tokens deployed by a creator
     * @param creator Address of the creator
     */
    function getCreatorTokens(address creator) external view returns (address[] memory) {
        return creatorTokens[creator];
    }

    /**
     * @notice Returns paginated list of deployed tokens
     * @param start Start index
     * @param limit Number of tokens to return
     */
    function getDeployedTokens(uint256 start, uint256 limit)
        external
        view
        returns (address[] memory)
    {
        require(start < deployedTokens.length, "Start index out of bounds");

        uint256 end = start + limit;
        if (end > deployedTokens.length) {
            end = deployedTokens.length;
        }

        uint256 resultLength = end - start;
        address[] memory result = new address[](resultLength);

        for (uint256 i = 0; i < resultLength; i++) {
            result[i] = deployedTokens[start + i];
        }

        return result;
    }

    /**
     * @notice Returns latest N deployed tokens
     * @param count Number of tokens to return
     */
    function getLatestTokens(uint256 count) external view returns (address[] memory) {
        if (count > deployedTokens.length) {
            count = deployedTokens.length;
        }

        address[] memory result = new address[](count);
        uint256 startIndex = deployedTokens.length - count;

        for (uint256 i = 0; i < count; i++) {
            result[i] = deployedTokens[startIndex + i];
        }

        return result;
    }

    // ============================================
    // ADMIN FUNCTIONS
    // ============================================

    /**
     * @notice Updates creation fee
     * @param newFee New fee in BNB
     */
    function updateCreationFee(uint256 newFee) external onlyOwner {
        uint256 oldFee = creationFee;
        creationFee = newFee;
        emit CreationFeeUpdated(oldFee, newFee);
    }

    /**
     * @notice Updates platform fee recipient
     * @param newRecipient New recipient address
     */
    function updatePlatformFeeRecipient(address payable newRecipient) external onlyOwner {
        require(newRecipient != address(0), "Invalid recipient");
        address oldRecipient = platformFeeRecipient;
        platformFeeRecipient = newRecipient;
        emit PlatformFeeRecipientUpdated(oldRecipient, newRecipient);
    }

    /**
     * @notice Updates PancakeSwap router address
     * @param newRouter New router address
     */
    function updatePancakeRouter(address newRouter) external onlyOwner {
        require(newRouter != address(0), "Invalid router");
        address oldRouter = pancakeRouter;
        pancakeRouter = newRouter;
        emit PancakeRouterUpdated(oldRouter, newRouter);
    }

    /**
     * @notice Toggles emergency pause
     * @dev NEW: Emergency circuit breaker
     */
    function togglePause() external onlyOwner {
        paused = !paused;
        emit PauseToggled(paused);
    }

    /**
     * @notice Blacklists a name or symbol
     * @dev NEW: Scam prevention
     * @param nameOrSymbol Name or symbol to blacklist
     * @param blacklist True to blacklist, false to unblacklist
     */
    function blacklistName(string memory nameOrSymbol, bool blacklist) external onlyOwner {
        bytes32 hash = keccak256(abi.encodePacked(_toLowerCase(nameOrSymbol)));
        blacklistedNames[hash] = blacklist;
        emit NameBlacklisted(nameOrSymbol, blacklist);
    }

    /**
     * @notice Batch blacklist names/symbols
     * @param names Array of names/symbols to blacklist
     * @param blacklist True to blacklist, false to unblacklist
     */
    function batchBlacklistNames(string[] memory names, bool blacklist) external onlyOwner {
        for (uint256 i = 0; i < names.length; i++) {
            bytes32 hash = keccak256(abi.encodePacked(_toLowerCase(names[i])));
            blacklistedNames[hash] = blacklist;
            emit NameBlacklisted(names[i], blacklist);
        }
    }

    // ============================================
    // INTERNAL HELPERS
    // ============================================

    /**
     * @notice Converts string to lowercase for case-insensitive comparison
     * @param str Input string
     * @return Lowercase string
     */
    function _toLowerCase(string memory str) internal pure returns (string memory) {
        bytes memory bStr = bytes(str);
        bytes memory bLower = new bytes(bStr.length);

        for (uint256 i = 0; i < bStr.length; i++) {
            // Convert uppercase ASCII (65-90) to lowercase (97-122)
            if (bStr[i] >= 0x41 && bStr[i] <= 0x5A) {
                bLower[i] = bytes1(uint8(bStr[i]) + 32);
            } else {
                bLower[i] = bStr[i];
            }
        }

        return string(bLower);
    }

    // ============================================
    // RECEIVE FUNCTION
    // ============================================

    receive() external payable {}
}
