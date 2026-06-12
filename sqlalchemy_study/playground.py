from sqlalchemy import create_engine
from os import getenv
from dotenv import load_dotenv, dotenv_values

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


con1 = engine.connect()  # connection to the DB
print('passowww')
con2 = engine.connect()  # connection to the DB

print(f'engine.pool.status \n{engine.pool.status()}\n')
# prints pool status, with all the connections in memory


print(f'connection \n{con1.connection.dbapi_connection}\n')
# prints the postgresql connector, no abstractions!

con1.close()  # closes the connection
