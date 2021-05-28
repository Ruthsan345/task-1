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


import os
#Db_URL="postgresql://tvmrhbjnytvuro:61a94c7df671bc80c67bfa75b48e76ad1c4b26634bac79a2dd0f74b51adde18f@ec2-107-22-245-82.compute-1.amazonaws.com:5432/do60c522tmtg3"
Db_URL="postgresql://postgres:swethA@127.0.0.1:5432/postgres"
database=databases.Database(Db_URL)
metadata=sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    Db_URL,
)
bank_details   = sqlalchemy.Table(
    "bank_details",
    metadata,
    sqlalchemy.Column("bank_id",sqlalchemy.INTEGER),
    sqlalchemy.Column("bank_name",sqlalchemy.String),
    sqlalchemy.Column("bank_ifsc",sqlalchemy.String),
    sqlalchemy.Column("bank_branch",sqlalchemy.String),
    sqlalchemy.Column("bank_address",sqlalchemy.String),
    sqlalchemy.Column("bank_city",sqlalchemy.String),
    sqlalchemy.Column("bank_district",sqlalchemy.String),
    sqlalchemy.Column("bank_state",sqlalchemy.String),
)


metadata.create_all(engine)





@app.on_event("startup")
async def startup():
    await database.connect()



@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/api/branches/autocomplete")
async def register_user(q:str,limit: int = 3, offsett: int = 0):
    auto=[]
    ret=[]
    print("hello")
    res=engine.execute('SELECT bank_branch FROM bank_details where bank_branch~*\'^'+str(q)+'\'').fetchall()
    for r in res:
        auto.append(r[0])
    auto=list(set(auto))
    for v in auto:
        query = bank_details.select().where(bank_details.c.bank_branch==v).offset(offsett).limit(limit).order_by(asc(bank_details.c.bank_ifsc))
        ret=ret+await database.fetch_all(query)
    return ret

@app.get("/api/branches/search")
async def register_user(q:str,limit: int = 3, offsett: int = 0):
        query = bank_details.select().where(bank_details.c.bank_city==q.upper()).offset(offsett).limit(limit).order_by(asc(bank_details.c.bank_ifsc))
        return await database.fetch_all(query)
