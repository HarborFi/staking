import pytest
import brownie
from brownie.test import given, strategy

@given(amount=strategy('uint256', min_value=1, max_value=2**256-1))
def test_valid_recover(accounts, staking, rToken, amount):
    print('amount: ', amount)
    # mint own mock tokens
    rToken.mint(amount, {'from': staking})
    txn = staking.recoverERC20(rToken, amount, {'from': accounts[0]})
    assert amount == txn.events['Recovered']['amount']
    assert rToken == txn.events['Recovered']['token']

@given(amount=strategy('uint256', min_value=1, max_value=2**256-1))
def test_invalid_recover(accounts, staking, rToken, amount):
    addr = 5
    with brownie.reverts():
        staking.recoverERC20(rToken, amount, {'from': accounts[addr]})

@given(amount=strategy('uint256', min_value=1, max_value=2**256-1))
def test_recover_with_staking_token(accounts, staking, sToken, amount):
    with brownie.reverts():
        staking.recoverERC20(sToken, amount, {'from': accounts[0]})