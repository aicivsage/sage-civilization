// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title IPancakeRouter02
 * @notice Minimal interface for PancakeSwap V2 Router
 * @dev Only includes functions required for automated liquidity provision
 *
 * This interface defines the essential PancakeSwap V2 Router functions needed
 * for the BondingCurveToken contract to programmatically add liquidity to
 * PancakeSwap when a token graduates from the bonding curve phase.
 *
 * Official PancakeSwap V2 Router on BNB Chain: 0x10ED43C718714eb63d5aA57B78B54704E256024E
 */
interface IPancakeRouter02 {
    /**
     * @notice Adds liquidity to a token/BNB pair on PancakeSwap
     * @dev Creates a new pair if it doesn't exist, or adds to existing pair
     *
     * @param token The BEP-20 token address
     * @param amountTokenDesired The amount of tokens to add as liquidity
     * @param amountTokenMin Minimum amount of tokens (slippage protection)
     * @param amountETHMin Minimum amount of BNB (slippage protection)
     * @param to Address to receive the LP tokens
     * @param deadline Unix timestamp after which the transaction will revert
     *
     * @return amountToken Actual amount of tokens added
     * @return amountETH Actual amount of BNB added
     * @return liquidity Amount of LP tokens minted
     */
    function addLiquidityETH(
        address token,
        uint256 amountTokenDesired,
        uint256 amountTokenMin,
        uint256 amountETHMin,
        address to,
        uint256 deadline
    )
        external
        payable
        returns (
            uint256 amountToken,
            uint256 amountETH,
            uint256 liquidity
        );

    /**
     * @notice Returns the address of Wrapped BNB (WBNB)
     * @dev Used to identify the BNB side of trading pairs
     * @return The WBNB token address
     */
    function WETH() external pure returns (address);

    /**
     * @notice Returns the address of PancakeSwap factory
     * @dev Used to query pair addresses
     * @return The factory contract address
     */
    function factory() external view returns (address);
}
