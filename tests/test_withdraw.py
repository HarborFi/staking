#!/usr/bin/python3
import pytest
import brownie
from brownie.test import given, strategy

@given(amount=strategy('uint256', min_value=1, max_value=100))
def test_valid_withdraw(accounts, staking, sToken, amount):
    addr = 4
    # mint own mock tokens
    sToken.mint(amount, {'from': accounts[addr]})
    # approve transfer to staking contract
    sToken.approve(staking, amount, {'from': accounts[addr]})
    assert sToken.balanceOf(accounts[addr]) == amount
    # stake tokens
    staking.stake(amount, {'from': accounts[addr]})
    assert staking.balanceOf(accounts[addr]) == amount
    assert staking.totalSupply() == amount
    print('rewards: ', staking.getReward({'from': accounts[addr]}))
    print('duration: ', staking.getRewardForDuration({'from': accounts[addr]}))
    # withdraw all tokens
    staking.withdraw(amount, {'from': accounts[addr]})
    assert staking.balanceOf(accounts[addr]) == 0
    assert staking.totalSupply() == 0
    # withdraw 1 more token than staked
    with brownie.reverts():
        staking.withdraw(1, {'from': accounts[addr]})

def test_invalid_withdraw(accounts, staking):
    addr = 5
    with brownie.reverts():
        staking.withdraw(0, {'from': accounts[addr]})
    assert staking.balanceOf(accounts[addr]) == 0
    assert staking.totalSupply() == 0