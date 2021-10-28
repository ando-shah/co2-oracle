#!/usr/bin/python3
from brownie import APIWeather, config, network
from web3 import Web3
from scripts.helpful_scripts import (
    get_account,
    get_contract,
)


def deploy_api_weather():
    jobId = config["networks"][network.show_active()]["jobId"]
    fee = config["networks"][network.show_active()]["fee"]
    account = get_account()
    oracle = get_contract("oracle").address
    link_token = get_contract("link_token").address
    api_weather = APIWeather.deploy(
        oracle,
        Web3.toHex(text=jobId),
        fee,
        link_token,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"API Weather deployed to {api_weather.address}")
    return api_weather


def main():
    deploy_api_weather()
