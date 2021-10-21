#!/usr/bin/python3
import pytest
import brownie
from brownie import chain
from brownie.test import given, strategy

@given(reward=strategy('uint256', min_value=1, max_value=2**256-1))
def test_valid_duration(accounts, staking, rToken, rewardsDistribution, reward):
    print('reward: ', reward)
    duration = chain.time()
    print('duration: ', duration)

    txn = staking.setRewardsDuration(duration, {'from': accounts[0]})
    assert txn.events['RewardsDurationUpdated']['newDuration'] == duration

    # allocate rewards to staking contract
    rToken.mint(reward, {'from': staking})
    # check reward token balance staking contract
    balance = rToken.balanceOf(staking)
    assert balance == reward

    # rough calculation of expected rate from notifyRewardAmount()
    rate = reward / duration
    # check reward rate is within is not too high
    if rate > balance / duration:
        reward = balance / duration
    print('reward: ', reward)

    txn = staking.notifyRewardAmount(reward, {'from': rewardsDistribution})
    assert txn.events['RewardAdded']['reward'] == reward
    # calculated reward rate
    rate = txn.events['RewardAdded']['rate'] 

    txn = staking.getRewardForDuration()
    print('rewards for duration: ', txn)
    assert txn == rate * duration

    # Previous rewards period must be complete before changing the 
    # duration for the new period
    duration = chain.time() + 1
    with brownie.reverts():
        staking.setRewardsDuration(duration, {'from': accounts[0]})

def test_invalid_duration(accounts, staking):
    addr = 4
    txn = staking.getRewardForDuration()
    # test a valid duration with invalid owner
    duration = chain.time()
    with brownie.reverts():
        staking.setRewardsDuration(duration, {'from': accounts[addr]})

@given(amount=strategy('uint256', min_value=1, max_value=2**256-1))
def test_valid_rewards(accounts, staking, sToken, rToken, rewardsDistribution, amount):
    print('amount: ', amount)
    reward = amount * 5
    print('reward: ', reward)
    addr = 4

    # allocate rewards to staking contract
    rToken.mint(reward, {'from': staking})
    # check reward token balance staking contract
    balance = rToken.balanceOf(staking)
    assert balance == reward

    # mint own mock tokens
    sToken.mint(amount, {'from': accounts[addr]})
    # approve transfer to staking contract
    sToken.approve(staking, amount, {'from': accounts[addr]})
    # stake tokens
    staking.stake(amount, {'from': accounts[addr]})
    assert staking.balanceOf(accounts[addr]) == amount

    txn = staking.notifyRewardAmount(reward, {'from': rewardsDistribution})
    assert txn.events['RewardAdded']['reward'] == reward

    # earn
    rewards_earned = staking.earned(accounts[addr])
    print('earned: ', rewards_earned)
    txn = staking.getReward({'from': accounts[addr]})
    if rewards_earned > 0:
        print("paid reward ({txn.events['RewardPaid']['user']}): {txn.events['RewardPaid']}")

@given(reward=strategy('uint256', min_value=0, max_value=2**256-1))
def test_invalid_rewards(accounts, staking, reward):
    with brownie.reverts():
        staking.notifyRewardAmount(reward)

@given(reward=strategy('uint256', min_value=0, max_value=2**256-1))
def test_reward_too_high(accounts, staking, rToken, rewardsDistribution, reward):
    duration = chain.time()
    # check reward token balance staking contract
    balance = rToken.balanceOf(staking)
    # make sure reward rate is too high
    if reward > balance / duration:
        with brownie.reverts():
            staking.notifyRewardAmount(reward, {'from': rewardsDistribution})

def test_last_time_reward(accounts, staking):
    period = staking.lastTimeRewardApplicable()
    print('lastTimeRewardApplicable: ', period)
