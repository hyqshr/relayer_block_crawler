from web3 import Web3
from sqlalchemy.orm import Session
from database import Block, Transaction  # Import your database models

def fetch_and_store_blocks(w3: Web3, db_session: Session, start_block: int, end_block: int) -> None:
    """
    Fetches blocks and their transactions from the Ethereum blockchain within a specified range
    and either updates existing records or inserts new records into the database.

    Args:
        w3 (Web3): An instance of Web3 connected to an Ethereum node.
        db_session (Session): A SQLAlchemy session bound to the database.
        start_block (int): The starting block number to fetch.
        end_block (int): The ending block number to fetch.

    Returns:
        None
    """
    for block_number in range(start_block, end_block + 1):
        try:
            block = w3.eth.get_block(block_number, full_transactions=True)
            if block:
                # Attempt to find an existing block record
                existing_block = db_session.query(Block).filter_by(number=block.number).first()

                if existing_block:
                    # Update the existing block record if found
                    existing_block.hash = block.hash.hex()
                    existing_block.timestamp = block.timestamp
                else:
                    # Create and add a new block record if not found
                    db_block = Block(number=block.number, hash=block.hash.hex(), timestamp=block.timestamp)
                    db_session.add(db_block)

                # Process transactions within the block
                process_transactions(block, db_session)

            # Commit changes for the current block to the database
            db_session.commit()
        except Exception as e:
            print(f"Error processing block {block_number}: {e}")
            db_session.rollback()  # Rollback in case of an error to avoid partial writes


def process_transactions(block: 'Block', db_session: Session) -> None:
    """
    Processes and updates or inserts transactions from a given block into the database.

    Args:
        block (Block): The block object containing transactions.
        db_session (Session): A SQLAlchemy session bound to the database.

    Returns:
        None
    """
    for tx in block.transactions:
        # Attempt to find an existing transaction record
        existing_transaction = db_session.query(Transaction).filter_by(hash=tx.hash.hex()).first()

        if existing_transaction:
            # Update existing transaction if found
            existing_transaction.block_number = block.number
            existing_transaction.from_address = tx['from']
            existing_transaction.to_address = tx['to']
            existing_transaction.value = Web3.from_wei(tx.value, 'ether')
        else:
            # Create and add a new transaction if not found
            db_tx = Transaction(
                hash=tx.hash.hex(),
                block_number=block.number,
                from_address=tx['from'],
                to_address=tx['to'],
                value=Web3.from_wei(tx.value, 'ether')
            )
            db_session.add(db_tx)
