import zoneinfo
from datetime import datetime
from fastapi import FastAPI

from models import Customer, CustomerCreate, Transaction, Invoice

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola mundo!"}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso= iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"Time": datetime.now(tz)}

db_customers: list[Customer] = []

@app.post("/customers", response_model=Customer)
async def create_customer( customer_data: CustomerCreate ):
    customer = Customer.model_validate( customer_data.model_dump() )
    
    db_customers.append(customer)
    customer.id = len(db_customers)
    return customer

@app.get("/customers", response_model=list[Customer])
async def list_customer():
    return db_customers

@app.post("/transactions")
async def create_transaction( transaction_data: Transaction ):
    return transaction_data

@app.post("/invoices")
async def create_invoice( invoice_data: Invoice ):
    return invoice_data