from dotenv import load_dotenv

from os import getenv

import sqlalchemy as sa

load_dotenv()
DATABASE_URL = str(getenv('DATABASE_URL'))


engine = sa.create_engine(DATABASE_URL)

metadata = sa.MetaData()

# REFLECTION:
user = sa.Table('user', metadata, autoload_with=engine)
"""reflects table "user" already existent in the DB.
        metadata.create_all(engine) doesnt inspect psql 
        DB to discover existing tables."""


# Creating table:
post = sa.Table(
    'post',
    metadata,
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id']),
)


metadata.create_all(engine)

inspector = sa.inspect(engine)

table_names = inspector.get_table_names()
print(table_names)
# returns ['comment', 'user', 'post']

"""

# INSPECT:
Allows access to schema details (table names, columns details)
-> Quick inspections without prior definitions


# REFLECTION: 
used when you need to alter the DB, so 
you dont have to define the whole db. you just
reflect the existent tables.
Loads information into Table objects
-> Creating structured representations of database tables


creating a Table object that reflects the DB tables
allows the usage of DQL (Data Query Language - read) and
DML (Data Manipulation Language - create, update and delete)
functions/methods.
"""
