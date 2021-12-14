#!/usr/bin/python3
from brownie import APICO2Ledger
from scripts.helpful_scripts import get_account
import datetime

api_contract = APICO2Ledger[-1]
account = get_account()


def read_all():
    count = api_contract.getEntityCount.call()
    print ("Total entries in Ledger: ", count)

    for i in range(count):
        key = api_contract.keyList(i)
        ts = datetime.datetime.fromtimestamp(key)

        print (f'Entry#{i+1} -> Timestamp: {ts}')
        
        t_budget, ppm, r_budget, owner = api_contract.getEntity.call(key,{"from": account},)

        print(f'[Total budget:{t_budget/10000} GtCO2e]|[Remaining Budget:{r_budget/10000} GtCO2e]|[Current CO2 concentration:{ppm/100} ppm]|[Requester ETH Address:{owner}]')


def main():

    print("Reading data from {}".format(api_contract.address))
    read_all()
      

