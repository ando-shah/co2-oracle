// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

contract APIWeather is ChainlinkClient {
    using Chainlink for Chainlink.Request;
    uint256 public tempMin;
    
    address private oracle; //Address type
    bytes32 private jobId;  
    uint256 private fee;    //in Link
    
    /**
     * Network: Kovan
     * Oracle: 0xc57b33452b4f7bb189bb5afae9cc4aba1f7a4fd8
     * Job ID: d5270d1c311941d0b08bead21fea7747
     * this Oracle can multiply the result
     * Fee: 0.1 LINK
     * Accessing weather data
     * Full details here: https://www.metaweather.com/api/
     * Woe ID : https://www.woeids.com/
     * Example, SF : WoeID = 2487956
     * https://www.metaweather.com/api/location/2487956/
     * We will retrieve min and max temperatures
     * Comes in format : consolidated_weather.0.min_temp / max_temp
     * e.g. 13.559999999999999
     * 15 decimal places

     */
    constructor(address _oracle, bytes32 _jobId, uint256 _fee, address _link) {
        if (_link == address(0)) {
            setPublicChainlinkToken();
        } else {
            setChainlinkToken(_link);
        }
        oracle = _oracle;
        // jobId = stringToBytes32(_jobId);
        jobId = _jobId;
        fee = _fee;
    }
    
    /**
     * Create a Chainlink request to retrieve API response, find the target
     * data, then multiply by 1000000000000000 (to remove decimal places from data).
     */
    function requestVolumeData(string memory _url) public returns (bytes32 requestId) 
    {
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
        
        // Set the URL to perform the GET request on
        // request.add("get", "https://www.metaweather.com/api/location/2487956/");
        request.add("get", _url);
        
        
        request.add("path", "consolidated_weather.0.min_temp"); //When you get the raw data, only grab what's at the end of this hierarchy
        
        // Multiply the result by 1000000000000000 to remove decimals
        int timesAmount = 10**15;
        request.addInt("times", timesAmount);
        
        // Sends the request
        return sendChainlinkRequestTo(oracle, request, fee);
    }
    
    /**
     * Receive the response in the form of uint256
     */ 
    function fulfill(bytes32 _requestId, uint256 temp) public recordChainlinkFulfillment(_requestId)
    {
        tempMin = temp;
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
