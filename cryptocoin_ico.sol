// cryptocoin ico

// version of compiler
pragma solidity ^0.7.4;

contract cryptocoin_ico {
    
    // introducting the total number of coins for sale
    uint256 ax_cryptocoin = 1000000;
    
    // introductory conversion rate from cryptocoin to USD
    uint256 public usd_to_cryptocoin = 1000;
    
    // total number of cryptocoins that have been bought by investors
    uint256 public total_cryptocoin_bought = 0;
    
    // mapping from the investor address to its equity in cryptocoin and USD 
    mapping(address => uint256) equity_cryptocoin;
    mapping(address => uint256) equity_usd;
    
    
    // check if an investor can buy cryptocoin
    modifier can_buy_cryptocoin(uint256 usd_invested) {
        require(usd_invested * usd_to_cryptocoin + total_cryptocoin_bought <= max_cryptocoin);
        _;
    }
    
    // TODO view is a write and needs to be a read -- for all of these functions!
    // getting the equity in cryptocoin of the investor
    function equity_in_cryptocoin(address investor) external view returns (uint256) {
        return equity_cryptocoin[investor];
    }
    
    // getting the equity in USD of the investor
    function equity_in_usd(address investor) external view returns (uint256) {
        return equity_usd[investor];
    }
    
    // buying cryptocoin
    function buy_cryptocoin(address investor, uint256 usd_invested) external
    can_buy_cryptocoin(usd_invested) {
        // coin is going to cap out real quick if uint128 applied ~= 4,000 usd max buy
        uint256 cryptocoin_bought = usd_invested * usd_to_cryptocoin;
        equity_cryptocoin[investor] += cryptocoin_bought;
        equity_usd[investor] = equity_cryptocoin[investor] / usd_to_cryptocoin;
        total_cryptocoin_bought += cryptocoin_bought;
    }

   // selling cryptocoin
    function sell_cryptocoin(address investor, uint256 cryptocoin_sold) external {
        equity_cryptocoin[investor] -= cryptocoin_sold;
        equity_usd[investor] = equity_cryptocoin[investor] / usd_to_cryptocoin;
        total_cryptocoin_bought -= cryptocoin_sold;
    }
}