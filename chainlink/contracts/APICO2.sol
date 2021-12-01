// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

contract APICO2 is ChainlinkClient {
    using Chainlink for Chainlink.Request;
    uint256 public co2_ppm;
    
    address private oracle; //Address type
    bytes32 private jobId;  
    uint256 private fee;    //in Link

    //Carbon budget variables
    uint256 public immutable co2_budget;
    uint256 public remaining_co2_budget;
    uint256 private immutable const;
    
    /**
     * Network: Kovan
     * Oracle: 0xc57b33452b4f7bb189bb5afae9cc4aba1f7a4fd8
     * Job ID: d5270d1c311941d0b08bead21fea7747
     * this Oracle can multiply the result
     * List of Oracle nodes & adapters on Testnets : https://docs.chain.link/docs/decentralized-oracles-ethereum-mainnet/
     * List of adapters on mainnet : https://market.link/search/adapters
     * Fee: 0.1 LINK
     * Accessing CO2 data from
     * Base API :https://co2ppm.herokuapp.com/
     * Params :
     * /trend :
     * /smoothed
     * 
     * Comes in format : co2_ppm
     * e.g. 450.00
     * 2 decimal places
     */
    constructor(address _oracle, bytes32 _jobId, uint256 _fee, address _link, uint256 _budget) {
        if (_link == address(0)) {
            setPublicChainlinkToken();
        } else {
            setChainlinkToken(_link);
        }
        oracle = _oracle;
        // jobId = stringToBytes32(_jobId);
        jobId = _jobId;
        fee = _fee;
        co2_budget = _budget;
        const = 781;
    }
    
    /**
     * Create a Chainlink request to retrieve API response, find the target
     * data, then multiply by 100 (to remove decimal places from data).
     */
    function requestCO2Data(string memory _url) public returns (bytes32 requestId) 
    {
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
        
        // Set the URL to perform the GET request on
        // request.add("get", "Base API :https://co2ppm.herokuapp.com/trend");
        request.add("get", _url);
        //When you get the raw data, only grab what's at the end of this hierarchy in the JSON
        request.add("path", "co2_ppm"); 
        
        // Multiply the result by 100 to remove decimals (e.g. co2_ppm = 415.92 -> 41592)
        int timesAmount = 100;
        request.addInt("times", timesAmount);
        
        // Sends the request
        return sendChainlinkRequestTo(oracle, request, fee);
    }
    
    /**
     * Receive the response in the form of uint256
     */ 
    function fulfill(bytes32 _requestId, uint256 data) public recordChainlinkFulfillment(_requestId)
    {
        co2_ppm = data;
        remaining_co2_budget = co2_budget - co2_ppm * const;
    }

    // function stringToBytes32(string memory source) public pure returns (bytes32 result) {
    //     bytes memory tempEmptyStringTest = bytes(source);
    //     if (tempEmptyStringTest.length == 0) {
    //         return 0x0;
    //     }

    //     assembly {
    //         result := mload(add(source, 32))
    //     }
    // }
}
