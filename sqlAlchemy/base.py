# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# docker run --name sql-orm-psql -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=usr -e POSTGRES_DB=sqlalchemy -p 5432:5432 postgres
engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
Session = sessionmaker(bind=engine)

Base = declarative_base()