from sqlalchemy import Column, Date, DateTime, String, DECIMAL, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(255), nullable=True)
    posting_date = Column(Date, nullable=True)
    transaction_date = Column(DateTime, nullable=True, unique=True)
    description = Column(String(255), nullable=True)
    original_description = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    money_out = Column(DECIMAL(10, 2), nullable=True)
    money_in = Column(DECIMAL(10, 2), nullable=True)
    fees = Column(DECIMAL(10, 2), nullable=True)
    balance = Column(DECIMAL(10, 2), nullable=True)
    group = Column(String(255), nullable=True)
