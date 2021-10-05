import datetime
import uuid
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from sqlalchemy import desc,asc
from fastapi.testclient import TestClient
app = FastAPI()

import databases, sqlalchemy
from database import  database,bank_details,engine




@app.on_event("startup")
async def startup():
    await database.connect()



@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/api/branches/autocomplete")
async def register_user(q:str,limit: int = 0, offsett: int = 0):
    auto=[]
    ret=[]
    print("hello")
    print(limit)
    res=engine.execute('SELECT bank_branch FROM bank_details where bank_branch~*\'^'+str(q)+'\'').fetchall()
    for r in res:
        auto.append(r[0])
    auto=list(set(auto))
    for v in auto:
        query = bank_details.select().where(bank_details.c.bank_branch==v).offset(offsett).limit(limit-1).order_by(asc(bank_details.c.bank_ifsc))
        ret=ret+await database.fetch_all(query)
    return ret

@app.get("/api/branches/search")
async def register_user(q:str,limit: int = 3, offsett: int = 0):
        query = bank_details.select().where(bank_details.c.bank_city==q.upper()).offset(offsett).limit(limit).order_by(asc(bank_details.c.bank_ifsc))
        return await database.fetch_all(query)
