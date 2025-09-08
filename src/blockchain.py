import datetime
import hashlib
import json

class OpenDAOBlockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.peers = set()
        self.credentials = {}

        # Create the genesis block
        self.create_block(previous_hash='1', proof=100)

    def create_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def create_transaction(self, sender, recipient, amount, data):
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'data': data
        })
        return self.get_last_block()['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - last_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def add_peer(self, address):
        self.peers.add(address)

    def issue_credential(self, user_id, credential_id, data):
        if user_id not in self.credentials:
            self.credentials[user_id] = []
        self.credentials[user_id].append({
            'credential_id': credential_id,
            'data': data,
            'timestamp': str(datetime.datetime.now())
        })
        return True

    def get_credentials(self, user_id):
        return self.credentials.get(user_id, [])

if __name__ == '__main__':
    # Example Usage
    blockchain = OpenDAOBlockchain()
    print("Genesis Block created:")
    print(json.dumps(blockchain.chain[0], indent=4))

    # Simulate a transaction
    blockchain.create_transaction(sender="0x123", recipient="0x456", amount=10, data={"course": "CS101"})
    
    # Mine a new block
    last_block = blockchain.get_last_block()
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(proof, previous_hash)

    print("\nNew Block mined:")
    print(json.dumps(block, indent=4))

    # Issue a credential
    blockchain.issue_credential(user_id="student123", credential_id="cert-cs101", data={"grade": "A"})
    print("\nCredentials for student123:")
    print(json.dumps(blockchain.get_credentials("student123"), indent=4))
