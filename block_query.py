from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database import Block, Transaction

def query_largest_volume_block(db_uri):
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    start_time = datetime(2024, 1, 1, 0, 0)
    end_time = datetime(2024, 1, 2, 0, 30)

    # Query to find the block with the highest sum of ether transfers
    result = session.query(
        Transaction.block_number,
        func.sum(Transaction.value).label('total_value')
    ).join(Block, Transaction.block_number == Block.number
    ).filter(
        Block.timestamp >= start_time.timestamp(),
        Block.timestamp <= end_time.timestamp()
    ).group_by(
        Transaction.block_number
    ).order_by(
        func.sum(Transaction.value).desc()
    ).first()

    if result:
        print(f"Block Number: {result.block_number}, Total Ether Transferred: {result.total_value} Ether")
    else:
        print("No transactions found in the given timeframe.")

    session.close()

if __name__ == '__main__':
    query_largest_volume_block("postgresql+psycopg2://user:huang@localhost/mydb")