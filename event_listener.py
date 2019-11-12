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
    contract_address = "0x1726029Be0D53711B87e1B94C8698753d7cA51DB"
    deposit_block_check=0
    exit_block_check=0

    with open("dlan-network/build/Contracts/DlanCore.json") as f:
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
                table.insert(dict(user=address, nft_a=0, nft_v=amount))
            deposit_block_check=int(deposit['blockNumber'])+1
        exit_events = my_contract.events.Exiting().createFilter(fromBlock=exit_block_check).get_all_entries()
        if exit_events:
            for ex in exit_events:
                print (ex['args'])
                address = ex['args']['owner']
                amount = ex['args']['a']
                user = table.find_one(user=address)
                if amount != user['nft_a']:
                    print ('SUBMIT CHALLENGE!')
                    print ('User claims: %s' % amount)
                    print ('Database shows: %s' % user['nft_a'])
                else:
                    print ('User exit matches database - Allow exit')
            exit_block_check=int(ex['blockNumber'])+1
        time.sleep(15)

if __name__=="__main__":main()
