import databases, sqlalchemy
import os
Db_URL="postgresql://tvmrhbjnytvuro:61a94c7df671bc80c67bfa75b48e76ad1c4b26634bac79a2dd0f74b51adde18f@ec2-107-22-245-82.compute-1.amazonaws.com:5432/do60c522tmtg3"
#Db_URL="postgresql://postgres:swethA@127.0.0.1:5432/postgres"
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




