#!/usr/bin/python3
import pytest
import brownie
from brownie.test import given, strategy

@given(amount=strategy('uint256', min_value=1, max_value=100))
def test_valid_staking(accounts, staking, sToken, amount):
    addr = 4
    # mint own mock tokens
    sToken.mint(amount, {'from': accounts[addr]})
    # approve transfer to staking contract
    sToken.approve(staking, amount, {'from': accounts[addr]})
    assert sToken.balanceOf(accounts[addr]) == amount
    # stake tokens
    staking.stake(amount, {'from': accounts[addr]})
    assert sToken.balanceOf(staking) == amount
    assert sToken.balanceOf(accounts[addr]) == 0
    assert staking.balanceOf(accounts[addr]) == amount
    assert staking.totalSupply() == amount

def test_invalid_staking(accounts, staking):
    addr = 5
    with brownie.reverts():
        staking.stake(0, {'from': accounts[addr]})
    assert staking.balanceOf(accounts[addr]) == 0
    assert staking.totalSupply() == 0

def test_pause_staking(accounts, staking, sToken):
    addr = 6
    amount = 25
    sToken.mint(amount, {'from': accounts[addr]})
    # approve transfer to staking contract
    sToken.approve(staking, amount, {'from': accounts[addr]})
    assert sToken.balanceOf(accounts[addr]) == amount
    # pause staking
    staking.pause({'from': accounts[0]})
    # stake own tokens
    with brownie.reverts():
        staking.stake(amount, {'from': accounts[addr]})
    assert staking.balanceOf(accounts[addr]) == 0
    assert staking.totalSupply() == 0
    # unpause staking
    staking.unpause({'from': accounts[0]})
    staking.stake(amount, {'from': accounts[addr]})
    assert sToken.balanceOf(staking) == amount
    assert sToken.balanceOf(accounts[addr]) == 0
    assert staking.balanceOf(accounts[addr]) == amount
    assert staking.totalSupply() == amount

def test_pause_permissions(accounts, staking):
    addr = 7
    with brownie.reverts():
        staking.pause({'from': accounts[addr]})
    with brownie.reverts():
        staking.unpause({'from': accounts[addr]})