#!/usr/bin/python3
import pytest
import brownie
from brownie.test import given, strategy

@given(amount=strategy('uint256', min_value=1, max_value=2**256-1))
def test_valid_exit(accounts, staking, sToken, amount):
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
    print('duration: ', staking.getRewardForDuration({'from': accounts[addr]}))
    # exit all tokens
    staking.exit({'from': accounts[addr]})
    assert staking.balanceOf(accounts[addr]) == 0
    assert staking.totalSupply() == 0
    # withdraw 1 more token than staked
    with brownie.reverts():
        staking.exit({'from': accounts[addr]})

def test_invalid_exit(accounts, staking):
    addr = 5
    with brownie.reverts():
        staking.exit({'from': accounts[addr]})
    assert staking.balanceOf(accounts[addr]) == 0
    assert staking.totalSupply() == 0