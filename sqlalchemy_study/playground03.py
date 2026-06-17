"""
Sometimes you want to make N transactions.
Connections enter the pool of connections
and each time connection is closed you need to get another one from the pool.

You can make many transactions and get many results at once
and specify the BEGIN
"""

from dotenv import load_dotenv
from os import getenv

from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = str(getenv('DATABASE_URL'))


engine = create_engine(DATABASE_URL)
query = 'select id, user_id, comment from "comment" limit 10 offset {of}'
# limit 10 -> 10 results
# offset -> retrieves a subset of rows (pagination)
# of -> determines which "page" of 10 rows will be retrieved

with engine.connect() as connection:
    # one connection generates many atomic transactions (ACID):
    with connection.begin():
        # presumes in the end it will be committed (if modified) or rolledback
        sql = text(query.format(of=0))  # retrieves from 0-9 (ids 1-10)
        result1 = connection.execute(sql)
    with connection.begin():
        sql = text(query.format(of=10))  # retrieves from 10-19 (ids 11-20)
        result2 = connection.execute(sql)
    with connection.begin():
        sql = text(query.format(of=20))  # retrieves from 20-29 (ids 21-30)
        result3 = connection.execute(sql)
