from blockchain import Blockchain
from wallet import Wallet

# Initialize the blockchain with a transaction limit
max_tx_per_block = 10
difficulty = 3
blockchain = Blockchain(
    max_transactions_per_block=max_tx_per_block, difficulty=difficulty
)

# Create wallets for users
users = {}
for i in range(10):
    user_id = f"User_{i}"
    users[user_id] = Wallet()

# Generate and add 100 signed transactions
transactions = []  # Store all created transactions for testing
for i in range(1, 102):
    sender_id = f"User_{i % 10}"
    recipient_id = f"User_{(i + 1) % 10}"
    amount = i * 0.1
    sender_wallet = users[sender_id]
    recipient_wallet = users[recipient_id]

    transaction = sender_wallet.create_transaction(recipient_wallet.address, amount)
    transactions.append(transaction)  # Keep track of transactions

    # last transcation will be used to test the invalid case of the transcation inclusion.
    if i <= 100:
        if blockchain.add_transaction(transaction):
            print(f"Transaction {i} added: {transaction}")
        else:
            print(f"Transaction {i} is invalid and was discarded.")

# Mine the transactions
print("Mining started...")
block_index = blockchain.mine()
if block_index:
    print(
        f"Mining completed. Blocks up to {block_index} have been added to the blockchain."
    )
else:
    print("No transactions to mine or mining failed.")

# Print the blockchain summary
print(blockchain)


#### START: TRANSACTION INCLUSION CHECK ####
# Case 1: both in a block and a chain
transaction_to_check = transactions[0]  # First transaction to check
block_to_check = 1  # Check block at index 1 (first mined block)

if blockchain.is_transaction_in_block(transaction_to_check, block_to_check):
    print(f"Transaction is in block {block_to_check}.")
else:
    print(f"Transaction is not in block {block_to_check}.")

# Check if a transaction is anywhere in the blockchain
if blockchain.is_transaction_in_chain(transaction_to_check):
    print("Transaction is in the blockchain.")
else:
    print("Transaction is not in the blockchain.")

# Case 2: Not in a block but in a chain
transaction_to_check = transactions[0]  # First transaction to check
block_to_check = 2  # Check block at index 2

if blockchain.is_transaction_in_block(transaction_to_check, block_to_check):
    print(f"Transaction is in block {block_to_check}.")
else:
    print(f"Transaction is not in block {block_to_check}.")


if blockchain.is_transaction_in_chain(transaction_to_check):
    print("Transaction is in the blockchain.")
else:
    print("Transaction is not in the blockchain.")

# Case 2: Not in a block, not in a chain
transaction_to_check = transactions[-1]  # Last transaction to check
block_to_check = 9  # Check block at index 9

if blockchain.is_transaction_in_block(transaction_to_check, block_to_check):
    print(f"Transaction is in block {block_to_check}.")
else:
    print(f"Transaction is not in block {block_to_check}.")

# Check if a transaction is anywhere in the blockchain
if blockchain.is_transaction_in_chain(transaction_to_check):
    print("Transaction is in the blockchain.")
else:
    print("Transaction is not in the blockchain.")

#### END: TRANSACTION INCLUSION CHECK ####


# Check if the blockchain is valid
if blockchain.is_chain_valid():
    print("Blockchain is valid.")
else:
    print("Blockchain is NOT valid.")

# Tampering with a block (invalidate the blockchain)
print("\nAttempting to tamper with the blockchain...\n")

# Tamper with a block by changing a transaction in block 1
block_to_tamper = blockchain.chain[1]  # Get block at index 1
tampered_transaction = block_to_tamper.transactions[0]
tampered_transaction.amount += 100  # Tamper with the amount

# Recompute the hash for the tampered block without recalculating PoW (invalid block)
block_to_tamper.hash = block_to_tamper.compute_hash()

# Check blockchain validity again after tampering
if blockchain.is_chain_valid():
    print("Blockchain is still valid after tampering.")
else:
    print("Blockchain is NOT valid after tampering.")
