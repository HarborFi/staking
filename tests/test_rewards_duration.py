#!/usr/bin/python3
import pytest
import brownie
from brownie import chain
from brownie.test import given, strategy

@given(amount=strategy('uint256', min_value=1, max_value=100))
def test_valid_duration(accounts, staking, sToken, amount):
    duration = chain.time()
    print('duration: ', duration)
    staking.setRewardsDuration(duration, {'from': accounts[0]})
    duration = chain.time() + 1
    print('duration: ', duration)
    staking.setRewardsDuration(duration, {'from': accounts[0]})

def test_invalid_duration(accounts, staking):
    addr = 4
    # test a valid duration with invalid owner
    duration = chain.time()
    with brownie.reverts():
        staking.setRewardsDuration(duration, {'from': accounts[addr]})