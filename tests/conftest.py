#!/usr/bin/python3

import pytest

@pytest.fixture(scope="module", autouse=True)
def rToken(MockToken, accounts):
    return MockToken.deploy(
        "reward token",
        "RWD",
        100, # 1e21,
        {'from': accounts[2]}
    )

@pytest.fixture(scope="module", autouse=True)
def sToken(MockToken, accounts):
    return MockToken.deploy(
        "staking token",
        "STK",
        100, # 1e21,
        {'from': accounts[1]}
    )

@pytest.fixture(scope="module", autouse=True)
def staking(StakingRewards, rToken, sToken, accounts):
    rewardsDistribution = accounts[3]
    return StakingRewards.deploy(
        rewardsDistribution,
        rToken,
        sToken,
        {'from': accounts[0]}
    )

@pytest.fixture(autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass
