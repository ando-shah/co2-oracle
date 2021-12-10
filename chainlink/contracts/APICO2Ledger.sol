// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

contract APICO2Ledger is ChainlinkClient {
    using Chainlink for Chainlink.Request;
    uint256 public co2_ppm;
    
    address private oracle; //Address type
    bytes32 private jobId;  
    uint256 private fee;    //in Link

    //Carbon budget variables
    uint256 public immutable total_co2_budget;
    uint256 public remaining_co2_budget;
    uint256 private immutable const;
    // string private url;
    address private sender;
    uint256 public last_timestamp;

    //Create the ledger
    struct ledgerStruct {
        uint256 total_co2_budget;
        uint256 co2_ppm;
        uint256 remaining_co2_budget;
        address owner;
        // uint256 timestamp;
        uint listPointer;
    }

    //It's key is the block timestamp, temporarily it's the address
    mapping (uint256 => ledgerStruct) private co2Ledger;
    //Array of keys -> TIMESTAMPs of requests
    uint256 [] public keyList;

    function isEntity(uint256 entityTimestamp) public returns(bool isIndeed) 
    {
        if(keyList.length == 0) return false;
        return (keyList[co2Ledger[entityTimestamp].listPointer] == entityTimestamp);
    }


    function getEntityCount() public returns(uint entityCount) 
    {
        return keyList.length;
    }
    error entryExists(uint256 ts, uint256 co2_ppm);

    function addEntity(uint256 entityTimestamp , uint256 t_budget, uint256 ppm, uint256 r_budget, address m_sender) private returns(bool success) 
    {
        if(isEntity(entityTimestamp)) revert entryExists({ts:entityTimestamp,co2_ppm:ppm});
        co2Ledger[entityTimestamp].co2_ppm = ppm;
        co2Ledger[entityTimestamp].remaining_co2_budget = r_budget;
        co2Ledger[entityTimestamp].owner = sender;
        co2Ledger[entityTimestamp].total_co2_budget = t_budget;
        keyList.push(entityTimestamp);
        co2Ledger[entityTimestamp].listPointer = keyList.length - 1; //Push returns the size of the array
        return true;
    }

    function getEntity(uint256 entityTimestamp) public returns(uint256 t_budget, uint256 ppm, uint256 r_budget, address m_sender)
    {
        assert(isEntity(entityTimestamp));
        return(
            co2Ledger[entityTimestamp].total_co2_budget,
            co2Ledger[entityTimestamp].co2_ppm,
            co2Ledger[entityTimestamp].remaining_co2_budget,
            co2Ledger[entityTimestamp].owner);
    }
    function getKeyAtIndex(uint index) public returns(uint256 key)
    {
        return keyList[index];
    }

    
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
        jobId = _jobId;
        fee = _fee;
        total_co2_budget = _budget;
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

        // url = _url;
        sender = msg.sender;
        last_timestamp = block.timestamp;
        
        // Sends the request
        return sendChainlinkRequestTo(oracle, request, fee);
    }


    /**
     * Receive the response in the form of uint256
     */ 
    function fulfill(bytes32 _requestId, uint256 data) public recordChainlinkFulfillment(_requestId)
    {
        co2_ppm = data;
        remaining_co2_budget = total_co2_budget - co2_ppm * const;

        //Log to ledger
        addEntity(last_timestamp, total_co2_budget, co2_ppm, remaining_co2_budget, sender);
       
    }


}
