//pragma solidity ^0.5.16;
pragma solidity ^0.8.7;

// SPDX-License-Identifier: MIT

// Inheritance
import "@openzeppelin/contracts/access/Ownable.sol";

// https://docs.synthetix.io/contracts/source/contracts/rewardsdistributionrecipient
abstract contract RewardsDistributionRecipient is Ownable {
    address public rewardsDistribution;

    function notifyRewardAmount(uint256 reward) external virtual;

    modifier onlyRewardsDistribution() {
        require(msg.sender == rewardsDistribution, "Caller is not RewardsDistribution contract");
        _;
    }

    function setRewardsDistribution(address _rewardsDistribution) internal virtual onlyOwner {
        rewardsDistribution = _rewardsDistribution;
    }
}