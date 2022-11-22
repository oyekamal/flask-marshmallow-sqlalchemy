# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create an engine
engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

# for database
# docker run --name sqlalchemy-orm-psql \
#     -e POSTGRES_PASSWORD=pass \
#     -e POSTGRES_USER=usr \
#     -e POSTGRES_DB=sqlalchemy \
#     -p 5432:5432 \
#     -d postgres

# docker run --name sql-orm-psql -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=usr -e POSTGRES_DB=sqlalchemy -p 5432:5432 postgres