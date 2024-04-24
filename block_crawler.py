import sys
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import Optional
from web3 import Web3

from ethereum import fetch_and_store_blocks

def connect_to_ethereum(rpc_endpoint: str) -> Optional[Web3]:
    """
    Connects to an Ethereum node using the specified JSON-RPC endpoint.

    Args:
        rpc_endpoint (str): The JSON-RPC URL to connect to the Ethereum node.

    Returns:
        Optional[Web3]: A Web3 instance connected to the specified Ethereum node, or None if connection fails.
    """
    w3 = Web3(Web3.HTTPProvider(rpc_endpoint))
    if w3.is_connected():
        logging.info("Successfully connected to Ethereum node.")
        return w3
    else:
        logging.error("Failed to connect to Ethereum node.")
        return None

def setup_database(db_uri: str):
    """
    Sets up the database connection and returns a session object.

    Args:
        db_uri (str): The connection URI for the database.

    Returns:
        Session: A session object bound to the database engine.
    """
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    return Session()

def main():
    """
    Main function to execute the block crawler script.
    """
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) != 4:
        logging.error("Usage: block_crawler.py <JSON-RPC endpoint> <SQLite path> <block range>")
        sys.exit(1)

    rpc_endpoint, db_uri, block_range = sys.argv[1], sys.argv[2], sys.argv[3]
    start_block, end_block = map(int, block_range.split('-'))

    w3 = connect_to_ethereum(rpc_endpoint)
    if not w3:
        sys.exit(1)  # Exit if connection to Ethereum node failed

    db_session = setup_database(db_uri)
    fetch_and_store_blocks(w3, db_session, start_block, end_block)

    db_session.close()

if __name__ == '__main__':
    main()
