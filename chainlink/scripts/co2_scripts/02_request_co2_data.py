#!/usr/bin/python3
from brownie import APICO2, config, network
from scripts.helpful_scripts import fund_with_link, get_account


#co2_base_url = "http://greenfi-api.herokuapp.com/"
co2_base_url = "https://co2ppm.herokuapp.com/"

# ToDos:
# Retrieve more than one field from the Oracle and parse it later
# 
# 

def request_co2(contract,account, param):
  url = co2_base_url + param
  request_tx = contract.requestCO2Data(url,{"from": account})
  request_tx.wait(1)
  print ("Request sent to API endpoint :", url)

#Only works for ether!
def check_balance(account):
    balance = account.balance()
    print ("Account Balance [ETH]: ", balance)
    if balance >= 1000000000000000000:
        return True
    return False


def main():
    account = get_account()

    api_contract = APICO2[-1]
    tx = fund_with_link(
        api_contract.address, amount=config["networks"][network.show_active()]["fee"]
    )
    tx.wait(1)

    request_co2(api_contract,account,"smoothed")
