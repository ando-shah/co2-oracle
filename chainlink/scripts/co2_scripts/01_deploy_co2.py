#!/usr/bin/python3
from brownie import APICO2, config, network
from web3 import Web3
from scripts.helpful_scripts import (
    get_account,
    get_contract,
)


def deploy_api_co2():
    jobId = config["networks"][network.show_active()]["jobId"]
    fee = config["networks"][network.show_active()]["fee"]
    account = get_account()
    oracle = get_contract("oracle").address
    link_token = get_contract("link_token").address
    api_co2 = APICO2.deploy(
        oracle,
        Web3.toHex(text=jobId),
        fee,
        link_token,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"API co2 deployed to {api_co2.address}")
    return api_co2


def main():
    deploy_api_co2()
