// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title IPancakeFactory
 * @notice Minimal interface for PancakeSwap V2 Factory
 * @dev Only includes the getPair function for verification purposes
 *
 * This interface provides access to the PancakeSwap Factory contract,
 * allowing verification that a liquidity pair has been properly created.
 *
 * Official PancakeSwap V2 Factory on BNB Chain: 0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73
 */
interface IPancakeFactory {
    /**
     * @notice Returns the address of a pair for two tokens
     * @dev Returns address(0) if the pair doesn't exist
     *
     * @param tokenA Address of the first token
     * @param tokenB Address of the second token (typically WBNB)
     * @return pair The address of the pair contract, or address(0) if it doesn't exist
     */
    function getPair(address tokenA, address tokenB) external view returns (address pair);
}
