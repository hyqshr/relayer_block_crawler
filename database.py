from sqlalchemy import create_engine, Column, Integer, String, BigInteger, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Block(Base):
    __tablename__ = 'blocks'
    number = Column(Integer, primary_key=True)
    hash = Column(String)
    timestamp = Column(BigInteger)

class Transaction(Base):
    __tablename__ = 'transactions'
    hash = Column(String, primary_key=True)
    block_number = Column(Integer, ForeignKey('blocks.number'))
    from_address = Column(String)
    to_address = Column(String)
    value = Column(Float)

def setup_database(db_uri):
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
