#!/usr/bin/python3
from brownie import APICO2Ledger
from scripts.helpful_scripts import get_account

api_contract = APICO2Ledger[-1]
account = get_account()


def read_all():
    count = api_contract.getEntityCount.call()
    print ("Ledger Count: ", count)

    for i in count:
        key = api_contract.keyList(i)
        print (f'Timestamp #{i}: {key}')
        
        t_budget, ppm, r_budget, owner = api_contract.getEntity.call(key,{"from": account},)

        print(f'[Total budget]:{t_budget}|[Remaining Budget]:{r_budget}|[Current CO2 ppm]:{ppm}|[Requester ETH Address]:{owner}')


def main():

    print("Reading data from {}".format(api_contract.address))
    if api_contract.co2_ppm() == 0:
      print("You may have to wait a minute and then call this again, unless on a local chain!")
    else:
      print ("Current CO2 concentration [parts per million]: ", api_contract.co2_ppm()/100)
      print ("Remaining CO2 budget [Gt-CO2] ", api_contract.remaining_co2_budget()/10000)
      print ("Timestamp [Epoch]: ", api_contract.last_timestamp())
      

