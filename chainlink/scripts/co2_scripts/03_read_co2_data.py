#!/usr/bin/python3
from brownie import APICO2


def main():
    api_contract = APICO2[-1]
    print("Reading data from {}".format(api_contract.address))
    if api_contract.co2_ppm() == 0:
      print("You may have to wait a minute and then call this again, unless on a local chain!")
    else:
      print("Current CO2 concentration [parts per million]: ", api_contract.co2_ppm()/100)
      print ("Remaining CO2 budget [Gt-CO2] ", api_contract.remaining_co2_budget()/10000)
      print ("Timestamp [Epoch]: ", api_contract.timestamp())
