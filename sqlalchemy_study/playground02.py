from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = str(getenv('DATABASE_URL'))

engine = create_engine(DATABASE_URL, echo=True)


"""
# Transaction w/o context manager (not ideal):

con = engine.connect()

sql = text('select id, user_id, comment from comments')

con.execute(sql)

con.close()    # needs closure

"""


# Transaction with context manager:

with engine.connect() as con:
    sql = text('select id, user_id, comment from comments')
    result = con.execute(sql)

"""
Fetching results:

Assigning the query to a variable allows you to fetch the result.

Queries results are special iterable objects called Result.
It implements many methods, including to fetch results:

result.fetchone() / .one() -> returns one. if result has more than one 
row, throws error

result.first() -> returns first row

result.fetchall() / .all() -> returns all rows in the result

result.fetchmany(num) / .partitions(num) -> return a number of rows equal 
to the passed argument.
"""


"""
# Async transactions:

a_engine = create_async_engine(DATABASE_URL)

async def main():
    async with a_engine.connect() as connection:
        a_sql = text('select id, user_id, comment from comments')
       a_result  = await connection.execute(a_sql)


run(main())
"""
