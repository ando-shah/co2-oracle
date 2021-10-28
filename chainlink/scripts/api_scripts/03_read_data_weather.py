#!/usr/bin/python3
from brownie import APIWeather


def main():
    api_contract = APIWeather[-1]
    print("Reading data from {}".format(api_contract.address))
    if api_contract.tempMin() == 0:
        print(
            "You may have to wait a minute and then call this again, unless on a local chain!"
        )
    print("Minimum Temp : ", api_contract.tempMin()/1000000000000000)
