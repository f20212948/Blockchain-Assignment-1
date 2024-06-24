<h1> Programming Assignemnt 1 <br> Blockchain Technology
<h2>Supply Chain Management

## Team Members : Team 06

<ol>
<li> Ninad Agrawal
<li> Aryan Saluja
<li> Abhishek Johi
<li> Vansh Gupta
<li> Om Mishra
</ol>
<hr>
<br>

## Classes :

### Transaction Class -

<li>Represents a transaction in the supply chain.
<li>Contains information about the order, product, timestamp, entities involved (manufacturer, distributor, client), status, verification, and a cryptographic signature.
<li>Includes methods for calculating the hash of the transaction.

### Blockchain Class -

<li>Represents the blockchain itself.
<li>Stores a chain of blocks (each containing multiple transactions).
<li>Manages pending transactions and mining new blocks.
<li>Provides methods for verifying the integrity of the blockchain and generating QR codes for orders.

### Client Class -

<li>Represents a client in the supply chain.
<li>Allows clients to place orders, confirm deliveries, add security deposits, and interact with the system.
<li>Clients are associated with a name, security deposit, and a list of orders.

### Distributor Class -

<li>Represents a distributor in the supply chain.
<li>Allows distributors to receive orders, send products, add security deposits, and interact with the system.
<li>Distributors are associated with a name, security deposit, and an indicator of their availability.

### Manufacturer Class -

<li>Represents the manufacturer in the supply chain.
<li>Allows manufacturers to add products, create orders, and interact with distributors and clients.
<li>Manufacturers are associated with a name, a product catalog, and a list of pending orders.

### Block Class -

<li>Represents a block in the blockchain.
<li>Contains an index, timestamp, a list of transactions, previous hash, nonce, difficulty, hash, and Merkle root.
<li>Implements methods for calculating the block's hash, mining the block, and building a Merkle tree for transactions.

## Functions Descriptions -

### def mine_block_POW(self) :

<li>The mine_block method is used to mine a block in the blockchain. It uses a proof-of-work algorithm to find a hash for the block that meets a certain difficulty level.
<li>The while loop runs until the hash of the block meets the difficulty level specified by self.difficulty. The difficulty level is represented by a string of 0s with a length equal to self.difficulty.
<li>The purpose of this method is to ensure that mining a block requires a certain amount of computational effort, which helps to prevent malicious actors from easily adding fraudulent blocks to the blockchain.

### def getQR(self,orderID):

<li>This function is a method of a blockchain class that generates a QR code for a given order ID. <li>It first searches for the order ID in the list of pending transactions and if found, it creates a dictionary containing the relevant information about the transaction and generates a QR code for it.<li> If the order ID is not found in the pending transactions, it searches for it in the blockchain and generates a QR code for the transaction if found.

### def approve_transactions(self):

<li> This function is a method of a blockchain class that approves transactions by verifying their authenticity. It iterates over the list of transactions in the blockchain and checks if a transaction has already been verified. If a transaction has already been verified, it skips it and moves on to the next one.
<li> If a transaction has not been verified , the method goes on to verify and assure that there is no conflict between a distributor and a client.
<li> It uses the signature attribute of the transaction class to make sure that the signatures of all {client , distributor , manufacturer} match to then confirm the transaction .If they don't match it deducts the security deposit accordingly.

### def build_merkle_tree(self) :

<li>This function is a method of a blockchain class that builds a Merkle tree for the list of transactions in the blockchain. It first creates a list of transaction hashes by iterating over the transactions in the blockchain and appending their hashes to the list.<li> If the number of transaction hashes is odd, it duplicates the last transaction hash to make it even, as a Merkle tree requires an even number of leaf nodes.<li> It then pairs up adjacent hashes and creates a new hash by concatenating them and hashing the result using SHA-256.<li> Finally, it returns the root hash of the Merkle tree.
