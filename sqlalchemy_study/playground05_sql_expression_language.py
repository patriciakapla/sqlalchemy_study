from dotenv import load_dotenv

from os import getenv

from sqlalchemy import create_engine, MetaData, Table, select, insert, update

from datetime import datetime

load_dotenv()
DATABASE_URL = str(getenv('DATABASE_URL'))


engine = create_engine(DATABASE_URL)

metadata = MetaData()

"""
Creating a Table object that reflects the DB tables
allows the usage of DQL (Data Query Language - read) and
DML (Data Manipulation Language - create, update and delete)
functions/methods.
This avoids the usage of the text() function, that sends a 
queries as strings (see playground02.py)
"""

user = Table('user', metadata, autoload_with=engine)

post = Table('post', metadata, autoload_with=engine)

comment = Table('comment', metadata, autoload_with=engine)

sql = select(user)

print(sql, '\n')

with engine.connect() as con:
    result = con.execute(sql)
    print(result.fetchmany(10), '\n')

# CompoundSelect -> builder of queries! builds a complex select

sql2 = (
    select(comment.c.user_id, user.c.username, comment.c.comment)
    .where(comment.c.user_id == 66)
    .join(user)
    .limit(10)
    .offset(0)
    .order_by(comment.c.id)
)

# adding logical operators to the queries: | = OR, & = AND
sql3 = (
    select(comment.c.user_id, user.c.username, comment.c.comment)
    # .where((comment.c.user_id == 66) | (comment.c.user_id == 7))
    .where(comment.c.user_id.in_([66, 7]))
    .join(user)
    .order_by(user.c.id)
)

with engine.connect() as con:
    result2 = con.execute(sql2)
    print(sql2)
    print(*result2.fetchall(), sep='\n', end='\n\n')
    result3 = con.execute(sql3)
    print(sql3)
    print(*result3.fetchall(), sep='\n')


# https://docs.sqlalchemy.org/en/20/core/sqlelement.html

# DML - also works as a builder for insert, update, delete


sql4 = insert(post).values(
    user_id=5, post='some gibberish', created_at=datetime(2006, 6, 6, 6, 6, 6)
)


with engine.connect() as con:
    con.execute(sql4)
    print()
    result = con.execute(select(post))
    for register in result:
        print(register)


sql5 = (
    update(comment)
    .where(
        comment.c.user_id == 1,
        comment.c.comment == 'Optimized asymmetric function',
    )
    .values(comment='PEI')
)

print(sql5)

sql6 = select(comment).where(
    comment.c.user_id == 1,
    comment.c.comment == 'PEI',
)

with engine.connect() as con:
    with engine.begin(): 
        result = con.execute(sql5)
        print(result.rowcount)
        con.commit()
    with engine.begin():
        result = con.execute(sql6)
        for row in result:
            print(row)
