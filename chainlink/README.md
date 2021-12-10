# Brownie Mix for Chainlink Oracle


## Prerequisites

Please install or have installed the following:

- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)
## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.


```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
# restart your terminal
pipx install eth-brownie
```
Or, if that doesn't work, via pip
```bash
pip install eth-brownie
```

2. Download the mix and install dependancies.

```bash
brownie bake chainlink-mix
cd chainlink-mix
pip install -r requirements.txt
```

This will open up a new Chainlink project. Or, you can clone from source:

```bash
git clone https://github.com/PatrickAlphaC/chainlink-mix
cd chainlink-mix
```

## Testnet Development
If you want to be able to deploy to testnets, do the following.

Set your `WEB3_INFURA_PROJECT_ID`, and `PRIVATE_KEY` [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).

You can get a `WEB3_INFURA_PROJECT_ID` by getting a free trial of [Infura](https://infura.io/). At the moment, it does need to be infura with brownie. If you get lost, you can [follow this guide](https://ethereumico.io/knowledge-base/infura-api-key-guide/) to getting a project key. You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.io/).

You'll also need testnet ETH and LINK. You can get LINK and ETH into your wallet by using the [faucets located here](https://docs.chain.link/docs/link-token-contracts). If you're new to this, [watch this video.](https://www.youtube.com/watch?v=P7FX_1PePX0). Look at the `rinkeby` and `kovan` sections for those specific testnet faucets. 

You can add your environment variables to a `.env` file. You can use the [.env.exmple](https://github.com/smartcontractkit/chainlink-mix/blob/master/.env.example) as a template, just fill in the values and rename it to '.env'. Then, uncomment the line `# dotenv: .env` in `brownie-config.yaml`

Here is what your `.env` should look like:
```
export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
export PRIVATE_KEY=<PRIVATE_KEY>
```

AND THEN RUN `source .env` TO ACTIVATE THE ENV VARIABLES
(You'll need to do this everytime you open a new terminal, or [learn how to set them easier](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html))


![WARNING](https://via.placeholder.com/15/f03c15/000000?text=+) **WARNING** ![WARNING](https://via.placeholder.com/15/f03c15/000000?text=+)

DO NOT SEND YOUR PRIVATE KEY WITH FUNDS IN IT ONTO GITHUB

Otherwise, you can build, test, and deploy on your local environment.

## Local Development

For local testing [install ganache-cli](https://www.npmjs.com/package/ganache-cli)
```bash
npm install -g ganache-cli
```
or
```bash
yarn add global ganache-cli
```

All the scripts are designed to work locally or on a testnet. You can add a ganache-cli or ganache UI chain like so:
```
brownie networks add Ethereum ganache host=http://localhost:8545 chainid=1337
```
And update the brownie config accordingly. There is a `deploy_mocks` script that will launch and deploy mock Oracles, VRFCoordinators, Link Tokens, and Price Feeds on a Local Blockchain.

## Running Scripts and Deployment

This mix provides a simple template for working with Chainlink Smart Contracts. The easiest way to start is to fork the mainnet chain to a local ganache chain. This will allow you to deploy local smart contracts to interact with the [Chainlink Price Feeds](https://docs.chain.link/docs/get-the-latest-price).

> NOTE: It's highly encouraged that you work with a local chain before testing on a testnet. You'll be a much faster developer!

### Compile

This will compile all the solidity code
```
brownie compile
```


### Chainlink CO2 API Call


This will deploy a smart contract to kovan and then make an API call via [Chainlink API Call](https://docs.chain.link/docs/make-a-http-get-request), to read the single CO2 concentration you requested
```
brownie run scripts/co2ledger__scripts/01_deploy_co2.py --network kovan
brownie run scripts/co2ledger__scripts/02_request_co2_data.py  --network kovan
# Request the data
brownie run scripts/co2ledger__scripts/03_read_co2_data.py --network kovan   
```

To read all the entries logged, use:
```
brownie run scripts/co2ledger_scripts/04_read_all.py --network kovan
```



### Local Development

Since we're using Oracles, the local infrastructure does not *currently* exist to support this, so for now, this mode is unsupported

## Testing

```
brownie test
```

For more information on effective testing with Chainlink, check out [Testing Smart Contracts](https://blog.chain.link/testing-chainlink-smart-contracts/)

Tests are really robust here! They work for local development and testnets. There are a few key differences between the testnets and the local networks. We utilize mocks so we can work with fake oracles on our testnets.

There is a `test_unnecessary` folder, which is a good exersize for learning some of the nitty-gritty of smart contract development. It's overkill, so pytest will skip them intentionally. It also has a `test_samples` folder, which shows an example Chainlink API call transaction receipt.


### To test development / local
```bash
brownie test
```
### To test mainnet-fork
This will test the same way as local testing, but you will need a connection to a mainnet blockchain (like with the infura environment variable.)
```bash
brownie test --network mainnet-fork
```
### To test a testnet
Kovan and Rinkeby are currently supported
```bash
brownie test --network kovan
```

## Adding additional Chains

If the blockchain is EVM Compatible, adding new chains can be accomplished by something like:

```
brownie networks add Ethereum binance-smart-chain host=https://bsc-dataseed1.binance.org chainid=56
```
or, for a fork:

```
brownie networks add development binance-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://bsc-dataseed1.binance.org accounts=10 mnemonic=brownie port=8545
```


## Getting LINK tokens

You will need LINK tokens in your metamask wallet to transact (even with the testnets). Dont worry, this can be achieved for free! To receive testnet Link tokens, go to your metamask wallet, and switch to the testnet of interest, say Kovan. Paste that address into:

https://faucets.chain.link/kovan
OR
https://kovan.chain.link/



## Linting

```
pip install black
pip install autoflake
autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .
black .
```

If you're using [vscode](https://code.visualstudio.com/) and the [solidity extension](https://github.com/juanfranblanco/vscode-solidity), you can create a folder called `.vscode` at the root folder of this project, and create a file called `settings.json`, and add the following content:

```json
{
  "solidity.remappings": [
    "@chainlink/=[YOUR_HOME_DIR]/.brownie/packages/smartcontractkit/chainlink-brownie-contracts@0.2.2",
    "@openzeppelin/=[YOUR_HOME_DIR]/.brownie/packages/OpenZeppelin/openzeppelin-contracts@4.3.2"
  ]
}
```
This will quiet the linting errors it gives you. 

## Resources

To get started with Brownie:

* [Chainlink Documentation](https://docs.chain.link/docs)
* Check out the [Chainlink documentation](https://docs.chain.link/docs) to get started from any level of smart contract engineering.
* Check out the other [Brownie mixes](https://github.com/brownie-mix/) that can be used as a starting point for your own contracts. They also provide example code to help you get started.
* ["Getting Started with Brownie"](https://medium.com/@iamdefinitelyahuman/getting-started-with-brownie-part-1-9b2181f4cb99) is a good tutorial to help you familiarize yourself with Brownie.
* For more in-depth information, read the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/)

## License

This project is licensed under the [MIT license](LICENSE).
