from pydantic import BaseModel

from typing import Optional

class CustomerBase(BaseModel):
    name: str
    description: Optional[str] = None
    email: str
    age: int

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: Optional[int] = None

class Transaction(BaseModel):
    id: int
    amount: int
    description: str

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def total(self):
        return sum( transaction.amount for transaction in self.transactions)