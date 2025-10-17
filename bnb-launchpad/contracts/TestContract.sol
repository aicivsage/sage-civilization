// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title TestContract
 * @notice Simple test contract to verify Hardhat compilation setup
 * @dev This contract will be replaced with actual launchpad contracts
 */
contract TestContract {
    string public message;
    uint256 public value;

    event MessageUpdated(string newMessage, uint256 timestamp);
    event ValueUpdated(uint256 newValue, uint256 timestamp);

    constructor() {
        message = "Hardhat setup successful!";
        value = 0;
    }

    /**
     * @notice Update the stored message
     * @param _newMessage The new message to store
     */
    function setMessage(string memory _newMessage) external {
        message = _newMessage;
        emit MessageUpdated(_newMessage, block.timestamp);
    }

    /**
     * @notice Update the stored value
     * @param _newValue The new value to store
     */
    function setValue(uint256 _newValue) external {
        value = _newValue;
        emit ValueUpdated(_newValue, block.timestamp);
    }

    /**
     * @notice Get both message and value in one call
     * @return The current message and value
     */
    function getAll() external view returns (string memory, uint256) {
        return (message, value);
    }
}
