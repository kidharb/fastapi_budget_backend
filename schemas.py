from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel

class CSVImportResponse(BaseModel):
    message: str
    imported_records: int

class TransactionBase(BaseModel):
    account_number: Optional[str] = None
    posting_date: Optional[date] = None
    transaction_date: Optional[datetime] = None
    description: Optional[str] = None
    original_description: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None
    money_out: Optional[float] = None
    money_in: Optional[float] = None
    fees: Optional[float] = None
    balance: Optional[float] = None
    group: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True
