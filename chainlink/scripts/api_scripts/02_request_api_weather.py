#!/usr/bin/python3
from brownie import APIWeather, config, network
from scripts.helpful_scripts import fund_with_link, get_account

base_url = "https://www.metaweather.com/api/location/"

# ToDos:
# Retrieve more than one field from the Oracle and parse it later
# 
# 


def main():
    account = get_account()
    api_contract = APIWeather[-1]
    tx = fund_with_link(
        api_contract.address, amount=config["networks"][network.show_active()]["fee"]
    )
    tx.wait(1)

    woeid = "2487956" #SF
    woeid = "2295386" #Kolkata

    url =  base_url + woeid + "/"

    request_tx = api_contract.requestWeatherData(url,{"from": account})
    request_tx.wait(1)
