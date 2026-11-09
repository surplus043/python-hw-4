import time
import asyncio
import datetime
import json

from enum import Enum
from pathlib import Path
from fastapi import FastAPI, status
from pydantic import BaseModel


class Reason(str, Enum):  # заводим причины обращения
    NO_NETWORK = "Нет доступа к сети."
    NO_PHONE_SERVICE = "Не работает телефон."
    BROKEN_EMAIL = "Не приходят письма."


class Inquiry(BaseModel):  # вводные данные для запроса
    surname: str
    name: str
    date_of_birth: datetime.date
    phone_number: str
    email: str

    # т.к. данные введены через enum, другие виды обращения будут отсеиваться с 422
    # третья задача, несколько причин обращения, set уберет дубликаты если они есть
    reasons: set[Reason]
    detection_time: datetime.datetime


app = FastAPI()


# API
@app.post('/customer')
async def create_inquiry(inquiry: Inquiry):
    # принять данные, перевести в json
    j = inquiry.model_dump_json()
    # время запроса + email пользователя, от которого идет обращение
    filename = str(datetime.datetime.now().strftime(
        "%Y-%m-%d_%H.%M.%S"))+'_'+inquiry.email+'.json'

    # проверить что файла нет
    f_path = Path('./storage/'+filename)
    if f_path.is_file():
        # файл с нынешним временем уже был сделан, надо подождать
        return status.HTTP_429_TOO_MANY_REQUESTS
    else:
        with f_path.open(mode="w", encoding="utf-8") as f:
            f.write(j)
        return status.HTTP_201_CREATED
