// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title MockPancakeRouter
 * @notice Mock implementation of PancakeSwap Router for testing
 * @dev Simulates liquidity addition and LP token creation
 */
contract MockPancakeRouter {
    address public immutable WETH;
    address public factory;

    // Track LP tokens created for each pair
    mapping(address => mapping(address => address)) public pairFor;

    event LiquidityAdded(
        address indexed token,
        uint256 tokenAmount,
        uint256 ethAmount,
        address indexed to
    );

    constructor(address _weth, address _factory) {
        WETH = _weth;
        factory = _factory;
    }

    /**
     * @notice Mock implementation of addLiquidityETH
     * @dev Creates a mock LP pair if it doesn't exist and transfers tokens
     */
    function addLiquidityETH(
        address token,
        uint amountTokenDesired,
        uint amountTokenMin,
        uint amountETHMin,
        address to,
        uint deadline
    ) external payable returns (
        uint amountToken,
        uint amountETH,
        uint liquidity
    ) {
        require(block.timestamp <= deadline, "EXPIRED");
        require(msg.value >= amountETHMin, "INSUFFICIENT_ETH");
        require(amountTokenDesired >= amountTokenMin, "INSUFFICIENT_TOKEN");

        // Transfer tokens from sender to router
        IERC20(token).transferFrom(msg.sender, address(this), amountTokenDesired);

        // Get or create LP pair
        address payable pair = payable(MockPancakeFactory(factory).getPair(token, WETH));
        if (pair == address(0)) {
            pair = payable(MockPancakeFactory(factory).createPair(token, WETH));
        }

        // Transfer tokens and ETH to pair
        IERC20(token).transfer(pair, amountTokenDesired);
        pair.transfer(msg.value);

        // Mint LP tokens to recipient
        uint256 lpTokens = MockPancakePair(pair).mint(to, amountTokenDesired, msg.value);

        emit LiquidityAdded(token, amountTokenDesired, msg.value, to);

        return (amountTokenDesired, msg.value, lpTokens);
    }
}

/**
 * @title MockPancakeFactory
 * @notice Mock implementation of PancakeSwap Factory for testing
 */
contract MockPancakeFactory {
    mapping(address => mapping(address => address)) public pairs;
    address[] public allPairs;

    event PairCreated(address indexed token0, address indexed token1, address pair, uint);

    function getPair(address tokenA, address tokenB) external view returns (address) {
        return pairs[tokenA][tokenB];
    }

    function createPair(address tokenA, address tokenB) external returns (address pair) {
        require(tokenA != tokenB, "IDENTICAL_ADDRESSES");
        require(pairs[tokenA][tokenB] == address(0), "PAIR_EXISTS");

        // Deploy new pair
        MockPancakePair newPair = new MockPancakePair(tokenA, tokenB);
        pair = address(newPair);

        pairs[tokenA][tokenB] = pair;
        pairs[tokenB][tokenA] = pair;
        allPairs.push(pair);

        emit PairCreated(tokenA, tokenB, pair, allPairs.length);
        return pair;
    }

    function allPairsLength() external view returns (uint) {
        return allPairs.length;
    }
}

/**
 * @title MockPancakePair
 * @notice Mock LP pair that simulates liquidity pool tokens
 */
contract MockPancakePair {
    address public token0;
    address public token1;

    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    constructor(address _token0, address _token1) {
        token0 = _token0;
        token1 = _token1;
    }

    receive() external payable {}

    function mint(address to, uint256 tokenAmount, uint256 ethAmount) external returns (uint256 liquidity) {
        // Simple liquidity calculation: sqrt(tokenAmount * ethAmount)
        liquidity = sqrt(tokenAmount * ethAmount);
        require(liquidity > 0, "INSUFFICIENT_LIQUIDITY_MINTED");

        totalSupply += liquidity;
        balanceOf[to] += liquidity;

        return liquidity;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        require(balanceOf[msg.sender] >= amount, "INSUFFICIENT_BALANCE");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        return true;
    }

    function sqrt(uint256 x) internal pure returns (uint256) {
        if (x == 0) return 0;
        uint256 z = (x + 1) / 2;
        uint256 y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
        return y;
    }
}

/**
 * @title MockWETH
 * @notice Mock Wrapped BNB for testing
 */
contract MockWETH {
    string public name = "Wrapped BNB";
    string public symbol = "WBNB";
    uint8 public decimals = 18;

    mapping(address => uint256) public balanceOf;

    event Deposit(address indexed dst, uint256 wad);
    event Withdrawal(address indexed src, uint256 wad);

    receive() external payable {
        deposit();
    }

    function deposit() public payable {
        balanceOf[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint256 wad) public {
        require(balanceOf[msg.sender] >= wad, "INSUFFICIENT_BALANCE");
        balanceOf[msg.sender] -= wad;
        payable(msg.sender).transfer(wad);
        emit Withdrawal(msg.sender, wad);
    }

    function transfer(address dst, uint256 wad) public returns (bool) {
        return transferFrom(msg.sender, dst, wad);
    }

    function transferFrom(address src, address dst, uint256 wad) public returns (bool) {
        require(balanceOf[src] >= wad, "INSUFFICIENT_BALANCE");
        balanceOf[src] -= wad;
        balanceOf[dst] += wad;
        return true;
    }
}
