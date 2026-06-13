from sqlalchemy import create_engine
from os import getenv
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = str(getenv('DATABASE_URL'))

# engine factory
engine = create_engine(
    DATABASE_URL,
    # echo= True
)

print(f'engine \n{engine}\n')


print(f'engine pool \n{engine.pool}\n')
# prints queue pool of connections (object), used to keep them in memory, since these are
# high cost processes


con1 = engine.connect()  # 1st connection to the DB

print(f'connection \n{con1.connection.dbapi_connection}\n')
# prints the postgresql connector, no abstractions!


# testing the connection pool

con2 = engine.connect()  # 2nd connection to the DB


con1.close()  # closes the 1st connection
con2.close()  # closes the 2st connection

con3 = engine.connect()  # 3nd connection to the DB


print(f'engine.pool.status \n{engine.pool.status()}\n')
# prints pool status, with all the connections in memory
