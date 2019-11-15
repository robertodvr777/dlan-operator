from flask import Flask, request #import main Flask class and request object
#from eth_keys import keys
from web3 import Web3
import dataset
import sys

app = Flask(__name__) #create the Flask app

#curl -d '{"nft_a":"400", "signature":"0x000765", "address":"0x7267b857B18080ECe4D006B55a8Ec2D1ccC37581"}' -H "Content-Type: application/json" -X POST http://localhost:5000/transaction

@app.route('/transaction', methods = ['POST'])
def transaction():
    #db = dataset.connect('sqlite:///database/users.db')
    db = dataset.connect('mysql://root:@localhost/radius')
    table = db['webserver_account']
    content = request.get_json()
    user = content['address']
    new_balance = content['nft_a']
    signature = content['signature']
    balance_update = dict(address=user, nft_a=new_balance)
    table.update(balance_update, ['address'])
    signature_update = dict(address=user, signature=signature)
    table.update(signature_update, ['address'])
    return 'Update Success'
    sys.exit(0)
    ''' STILL NEED TO IMPLEMENT VERIFICATION
    nft_value = request.args.get('a')
    hashed_message = Web3.keccak(int(new_balance))
    print (hashed_message.hex())
    print ('0xe71fac6fb785942cc6c6404a423f94f32a28ae66d69ff41494c38bfd4788b2f8')
    print (nft_value)
    message = request.args.get('signature')
    signature_bytes = bytes.fromhex(message)
    signature = keys.Signature(signature_bytes)
    print (signature)
    message_key = signature.recover_public_key_from_msg(hashed_message)
    ### STILL NEED VERIFICATION ###
    #print (message_key)
    #print (message_key == user_public_key)
    #print (signature.verify_msg(hashed_message, user_public_key))
    ### STILL NEED VERIFICATION ###
    '''
    return '''<h1>Received tokens: {}</h1>'''.format(nft_value)

@app.route('/balance', methods = ['GET'])
def balance():
    db = dataset.connect('sqlite:///database/users.db')
    table = db['users']
    address = request.args.get('address')
    print (address)
    user = table.find_one(address=address)
    print (user)
    #return '''<h1>User Balance: {}</h1>'''.format(user['nft_a'])
    return str(user['nft_a'])


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=5000) #run app in debug mode on port 5000