
from fastapi import APIRouter, HTTPException, Query, status
from db import SessionDep
from models import Customer, Transaction, TransactionCreate
from sqlmodel import select


router = APIRouter(tags=['Transactions'])

@router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction( transaction_data: TransactionCreate, session: SessionDep ):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get('customer_id'))

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exists")
    
    transaction_db = Transaction.model_validate( transaction_data_dict )

    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)

    return transaction_db

@router.get("/transactions")
async def list_transaction(session: SessionDep, skip: int = Query(0, description="Registros a omitir"), limit: int = Query(10, description="Numero de registros")):
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()
    return transactions