import hashlib
import requests
import json
import sys
from blockchain import Blockchain

# TODO: Implement functionality to search for a proof 
b= Blockchain()
def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    # TODO
    
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:6] == "000000"


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    :return: A valid proof for the provided block
    """
    # TODO
    

    block_string = json.dumps(block,sort_keys = True).encode()

    proof = 0
    while valid_proof(block_string,proof) is False:
        proof += 1

    return proof


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:6000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        last_proof = requests.get(f"{node}/last_block")

        # TODO: When found, POST it to the server {"proof": new_proof}
        # print(last_proof.text)
        proof = proof_of_work(last_proof.text)
        # print(proof)

        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        if(proof):
            response = requests.post(f"{node}/mine", data={'proof':proof})
            str_response = json.loads(response.text)
            # print(str_response["message"])

        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
            if(str_response['message']== 'New Block Forged'):
                coins_mined += 1
                print(f'coins_mined: {coins_mined}')
            else:
                print(str_response['message'])
        
        
        
