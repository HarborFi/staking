pragma solidity ^0.8.7;

// SPDX-License-Identifier: MIT

//import "OpenZeppelin/openzeppelin-contracts@4.3.1/contracts/token/ERC20/extensions/ERC20Capped.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Capped.sol";
//import "OpenZeppelin/openzeppelin-contracts@4.3.1/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "@openzeppelin/contracts/access/AccessControlEnumerable.sol";

/// @title Mock token contract
/// @author Quad team
/// @notice testing purposes for Staking contract
contract MockToken is ERC20Capped, AccessControlEnumerable {
    using SafeERC20 for IERC20;

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    /// @notice when tokens are minted, this event is fired
    /// @param from address tokens are minted for
    /// @param amount of tokens to mint
    event Minted(address from, uint256 amount);

    /// @notice smart contract constructor
    /// @param name of the ERC20 token to create
    /// @param symbol of the token
    /// @param supply - total supply of the capped token
    constructor(string memory name, string memory symbol, uint256 supply)
        ERC20(name, symbol)
        ERC20Capped(supply * 10 ** 18)
    {
        _setupRole(DEFAULT_ADMIN_ROLE, _msgSender());
        _setupRole(MINTER_ROLE, _msgSender());
    }

    /// @notice this function mints tokens. it is only callable by an address with minter privileges
    /// @param amount of tokens to be minted
    function mint(uint256 amount) external virtual
    {
        require(_msgSender() != address(0), "Invalid recipient address");
        require(amount > 0, "Amount must be greater than 0");
        ERC20._mint(_msgSender(), amount);
        emit Minted(_msgSender(), amount);
    }

    /// @notice verifies the type of smart contract support
    /// @dev See {IERC165-supportsInterface}.
    /// @param interfaceId id to be verified whether it's compatible with this smart contract
    /// @return true or false whether the interface is supported by this smart contract
    function supportsInterface(bytes4 interfaceId) public view virtual override returns (bool) 
    {
        return interfaceId == type(IERC20).interfaceId || super.supportsInterface(interfaceId);
    }
}
