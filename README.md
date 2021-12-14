# Carbon Dioxide Oracle - CO2O

This project's goals are:

- Deliver realtime carbon dioxide (CO2) concentration data, aggregated from National Oceanic and Atmospheric Administration’s (NOAA) Global Monitoring Lab, to any smart contract on the Ethereum network
- Compute the remaining carbon budget from this data point
- Immutably log the inputs and outputs that led to this outcome to an on-chain database
- Allow any web3 client to query this database

This in effect acts as a framework for illuminating carbon pricing supply chains. The next step is to extend this framework to do carbon pricing and logging as well. The longer term goals of this project are to enable open access carbon pricing to anyone (web or web3 clients), with a corresponding log to a public blockchain, and subsequent retrieval.

The software architcecture is as show below: 
![Software Architecture](/images/CO2-OracleSystem-Diagram.png)


There are two major components in this project:

## CO2 API
The de facto source of atmospheric carbon dioxide concentration is from the National Oceanic and Atmo- spheric Administration’s (NOAA) Global Monitoring Lab, which publishes greenhouse gas concentration readings from 87 stations around the world, at intervals ranging from hourly to monthly, with some unpredictable lag. Originally, we planned to create a model that would predict the realtime (hourly) outcome from the daily and weekly values, which would account for the seasonal nature of CO2 concentration change[^1], but we found that NOAA already publishes two sets of predicted values on a daily basis that model the global average CO2 concentration (’smoothed’), and control for the seasonal differences (’trend’). These were accurate and high frequency enough for our purposes. However NOAA does not provide an API for this data, but simply a text file download. To fill this gap, we created a simple CO2 server, built on Flask, that would scrape this data from NOAA on a daily basis, perform some data cleaning and store these values in a database. This data, along with it’s generated timestamp were exposed through an API that allows anyone to read the most recent CO2 concentration values (both smoothed and trend) along with an epoch timestamp. This API would enable this data to be brought on chain.

### Implementation

All implementation details for this Flask server can be found below:

[API Readme](API/README.md)

## Smart Contracts
As specified earlier, the SCs have a dual function: to fetch the cost of carbon from the CO2 Oracle and derive the carbon budget, and create an immutable entry to the underlying blockchain with the timestamp, and all input parameters. This schema encapsulates all the constituents that led to this particular price, rendering the supply chain transparent. To fetch the realtime data from the CO2 Oracle, we used the request-response mechanism, as required by Chainlink’s hybrid smart contracts. They require two separate calls to the SC: the first specifying the API endpoint and JSON hierarchy, and a second to read the retrieved data. The second call is also used to compute the carbon budget on-chain. In order to immutably log this schema, we created a limited functionality CRUD database (without the update and delete functions), that allows for append as well as sequential and random reads. We adapted Rob Hitchen’s CRUD framework[^2] to use a private Mappings as the hash table, with the timestamp as the unique key, and all the input parameters and generated output within a struct, as the storage. In order to allow web3 clients to iterate over the keys and retrieve any element without loosening the security of the hash table, we add a public dynamic array to store the keys:
```
mapping ( uint256 => ledgerStruct ) private co2Ledger ; uint256 [] public keyList ;
```
To enable any web3 client to iterate over the entire database and retrieve any or all entries, we expose the following functions:
```
function getEntityCount () public returns ( uint entityCount ) function getEntity(uint256 entityTimestamp) public returns (...) 
function getKeyAtIndex(uint index) public returns(uint256 key)
```

### Implementation
The smart contract implementation and testing was done using the Brownie Frame- work which is a Python-based development and testing framework for smart contracts on Ethereum. Smart contracts were written in Solidity (v0.8). This framework enabled us to write sophisticated web3 client-side interaction scripts. This smart contract has been deployed to the Kovan testnet at 0xD56f9457961fE6C02B791c666Fba2830a510DD78. All code and instructions to replicate this system are available on Github. The CO2 concentration API can be accessed at https://co2ppm.herokuapp.com/trend.

The Brownie code for this implementation and details to recreate it can be found below:

[Chainlink Readme](chainlink/README.md)



## License

This project is licensed under the [MIT license](LICENSE).

[^1]: This seasonal variation is because during the northern hemisphere summer, the vegetation around the equator and in the northern hemisphere absorb large amounts of CO2 during photosynthesis, and during the northern hemisphere winter, this activity shifts southwards where there are relatively fewer photosynthesizing agents.
[^2]: Rob Hitchens. Solidity CRUD part 1 URL: https://medium.com/robhitchens/solidity-crud-part-1-824ffa69509a.

