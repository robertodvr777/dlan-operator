import json
from web3.providers.rpc import HTTPProvider
from web3 import Web3
from web3.contract import ContractEvent
import dataset
import time

def handle_event(event):
    print("Event triggered")


def main():
    db = dataset.connect('sqlite:///database/users.db')
    table = db['users']
    w3 = Web3(HTTPProvider('http://localhost:7545'))
    contract_address = "0xCE7001904DfF8adF14C92243306BCb39879fEb7A"
    deposit_block_check=0
    exit_block_check=0

    with open("../dlan-network/build/Contracts/DlanCore.json") as f:
        info_json = json.load(f)
    abi = info_json["abi"]

    my_contract = w3.eth.contract(address=contract_address, abi=abi)
    while True:
        deposit_events = my_contract.events.Deposited().createFilter(fromBlock=deposit_block_check).get_all_entries()
        if deposit_events:
            for deposit in deposit_events:
                print (deposit['args'])
                print (deposit['blockNumber'])
                address = deposit['args']['owner']
                amount = deposit['args']['_numberOfDlanTokens']
                table.insert(dict(address=address, bal=amount, signature='d956de560b45429ea0a8a64afafe4b0a3b0e5c54d0f4ca5c1a760af1a6cdcf6b4c8d58a14f5b482f6d2750ac076723a89554c5c19efab2441ceeaac6a82c27f51b'))
            deposit_block_check=int(deposit['blockNumber'])+1
        exit_events = my_contract.events.Exiting().createFilter(fromBlock=exit_block_check).get_all_entries()
        if exit_events:
            for ex in exit_events:
                print (ex['args'])
                address = ex['args']['owner']
                amount = ex['args']['bal']
                user = table.find_one(address=address)
                if amount != user['bal']:
                    print ('SUBMIT CHALLENGE!')
                    print ('User claims: %s' % amount)
                    print ('Database shows: %s' % user['bal'])
                    challenge = my_contract.functions.challenge(user['address'],user['bal'],user['signature']).call()
                else:
                    print ('User exit matches database - Allow exit')
                    challenge = my_contract.functions.challenge(user['address'],user['bal'],user['signature']).call()
            exit_block_check=int(ex['blockNumber'])+1
        time.sleep(15)

if __name__=="__main__":main()
