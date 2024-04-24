# Ethereum Block Crawler

The Ethereum Block Crawler is a Python script designed to retrieve Ethereum blockchain data within a specified block range and persist it to a database. It provides functionality to connect to an Ethereum node, fetch blocks and transactions, and store them in a relational database. Additionally, it includes a feature to query the database for the block with the largest volume of ether transferred within a given timeframe.

## Features

- Connect to an Ethereum node via JSON-RPC endpoint.
- Fetch Ethereum blockchain data (blocks and transactions) within a specified block range.
- Store fetched data in a relational database (SQLite or PostgreSQL).
- Query the database for the block with the largest volume of ether transferred within a given timeframe.
- Production-level error handling and logging.

## Installation

1. Clone this repository to your local machine:

2. Install dependency:
Go to project folder:

```
pip install -r requirements.txt
```

## Usage

### 1. Fetch Ethereum Blockchain Data

To fetch Ethereum blockchain data and store it in a database, run the following command:

```
python block_crawler.py <JSON-RPC endpoint> <SQLite/PostgreSQL path> <block range>
```

### 2. Query Largest Volume Block
```
python block_query.py
```