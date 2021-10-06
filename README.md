# StakingRewards

StakingRewards is a staking smart contract developed using the brownie framework.

# External Libraries

This project relies on OpenZeppelin libraries version v4.3.1.

> npm install @openzeppelin/contracts

## Basic Use

To interact with a deployed contract in a local environment, start by opening the console:

```bash
brownie console
```

## Testing

To modify the deployment logic, edit the [`tests/conftest.py::token`](tests/conftest.py) fixtures.

To execute the unit tests defined in the tests/ folder, run the following command:

```bash
brownie test -s --update --interactive
```

    -s: prints out to the console output from print()
    --update: only runs the new test cases
    --interactive: breaks into the console. this allows debugging when a failed assert occurs

When calling a Solidity function, the returned result is the txn instead of the value. To get the value, add '.call()' to the end of the function name.

To verify your test coverage, use the following flag:

```bash
brownie test --coverage
```

## Scripts

TBD