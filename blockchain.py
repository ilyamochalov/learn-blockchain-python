from time import time
import json
import hashlib


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Creates genesis block
        # self.new_block()

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new block in the Blockchain
        :param proof: <init> The proof given by teh Proof of Work Algorithm
        :param previous_hash: <str> Optional hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transaction': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []

        self.chain.append(block)

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        """Returns the last Block in the Chain"""
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    def proof_of_work(self, last_proof):
        """
        Proof of work algorithm

        :param last_proof: <int> previous proof of work
        :return: <int> proof of work
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof: Does the hash(last_proof, proof) contain 4 leading zeroes?

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, false if not
        """

        return hashlib.sha256(f'{last_proof}{proof}'.encode()).hexdigest()[:4] == '0000'
