import time
import asyncio
import datetime
import json

from pathlib import Path
from fastapi import FastAPI, status
from pydantic import BaseModel


class Customer(BaseModel):  # вводные данные для запроса
    surname: str
    name: str
    date_of_birth: datetime.date
    phone_number: str
    email: str


app = FastAPI()


# API
@app.post('/customer')
async def create_customer(customer: Customer):
    # принять данные, перевести в json
    j = customer.model_dump_json()
    # время запроса + email пользователя, от которого идет обращение
    filename = str(datetime.datetime.now().strftime(
        "%Y-%m-%d_%H.%M.%S"))+'_'+customer.email+'.json'
    
    # проверить что файла нет
    f_path = Path('./storage/'+filename)
    if f_path.is_file():
        # файл с нынешним временем уже был сделан, надо подождать
        return status.HTTP_429_TOO_MANY_REQUESTS
    else:
        with f_path.open(mode="w", encoding="utf-8") as f:
            f.write(j)
        return status.HTTP_201_CREATED
