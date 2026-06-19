"""
Object Relational Mapper (O/R Mapper)

mapping of the metadata of a table into a class.
each row is related to an instance


*different models and ways of declaring it:*

declarative definition:

    traditional classes (w/o type hints or dataclass)

    type hints
        use of sqlalchemy.orm Mapped class and mapped_column():
        attribute: Mapped[str] = mapped_column(...)

    dataclasses
        from sqlalchemy.orm import registry
        reg = registry()
        @reg.mapped_as_dataclass
        class definition

        -> becomes necessary to declare init=True or False

imperative definition

automapping
    events
"""

from datetime import datetime

from dotenv import load_dotenv

from os import getenv

from sqlalchemy import (
    Column,
    Integer,
    String,
    func,
    ForeignKey,
    TIMESTAMP,
    Table,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
    create_engine
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    registry
)


# DECLARATIVE: REGULAR CLASSES (w/o dataclass or type hints)


class Base(DeclarativeBase): ...


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)


# DECLARATIVE: REGULAR CLASSES with TYPE HINTS


class Post(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), server_default=func.now()
    )


# DECLARATIVE: DATACLASS - must have type hints!!

reg = registry()


@reg.mapped_as_dataclass
class Comment:
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    # init=False tells the constructor to not expect an argument for the attr
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    comment: Mapped[str]
    post_id: Mapped[int | None] = mapped_column(ForeignKey('post.id'))
    live_id: Mapped[int | None] = mapped_column(ForeignKey('live.id'))


# IMPERATIVE

mapper_registry = registry()

live_table = Table(
    'live',
    mapper_registry.metadata,
    Column('id', Integer(), nullable=False),
    Column('user_id', Integer(), nullable=False),
    Column('platform', String(), nullable=False),
    Column('created_at', TIMESTAMP(timezone=False), nullable=False),
    PrimaryKeyConstraint('id'),
    ForeignKeyConstraint(['user_id'], ['user.id']),
)


class Live:
    pass


mapper_registry.map_imperatively(Live, live_table)


# SCHEMA CREATION USING REGISTRY() - more explicit, lower level, usually with dataclasses

load_dotenv()
DATABASE_URL = str(getenv('DATABASE_URL'))

engine = create_engine(DATABASE_URL)


reg.metadata.create_all(engine)
# in sqlalchemy's core, the Metadata class is the container with
# all the table definitions from mapped classes.
# in ORM, the registry() class has the metadata inside it.
# create_all() creates all the database objects mapped to metadata.
# Python class (-mapping->) table definition/MetaData (-create_all->)
# physical table in PostgreSQL


# SCHEMA CREATION USING THE DECLARATIVE BASE - implements registry() behind the scenes

Base.metadata.create_all(engine)


# mixing registry() and declarative base schemas can go wrong!
# each one creates a different object, so the tables in each wont see
# the others'!
# in this example, Base.metadata stores User and Post, reg.metadata stores Comment
# and mapper_registry.metadata will store Live



# creating an instance

Comment(
    user_id=3,
    comment='what a beautiful wedding, said the bridesmade to the waiter',
    post_id=3,
    live_id=None,
)
