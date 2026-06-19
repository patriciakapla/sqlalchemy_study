from os import getenv

from dotenv import load_dotenv

from datetime import datetime

from sqlalchemy import ForeignKey, TIMESTAMP, func, create_engine, select

from sqlalchemy.orm import registry, Mapped, mapped_column, Session

load_dotenv()

DATABASE_URL = str(getenv('DATABASE_URL'))

engine = create_engine(DATABASE_URL)

reg = registry()


@reg.mapped_as_dataclass
class User:
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


@reg.mapped_as_dataclass
class Post:
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), server_default=func.now()
    )


@reg.mapped_as_dataclass
class Live:
    __tablename__ = 'live'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    platform: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), server_default=func.now()
    )


@reg.mapped_as_dataclass
class Comment:
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    comment: Mapped[str]
    post_id: Mapped[int | None] = mapped_column(ForeignKey('post.id'))
    live_id: Mapped[int | None] = mapped_column(ForeignKey('live.id'))


reg.metadata.create_all(engine)


Comment(
    user_id=3,
    comment='what a beautiful wedding, said the bridesmade to the waiter',
    post_id=3,
    live_id=None,
)


"""
SESSION -> manages transactions! communication between python objects and DB.
    implements abstraction for the connection, begin, end, etc.
    and still creates object cache in memory (actually an identity map) of each loaded row
"""

with Session(engine) as s:
    result = s.scalar(select(Comment).where(Comment.user_id == 3))
    print(  # scalar returns a single value
        result
    )

'''
the result is an object:
Comment(id=204, user_id=3, comment='Automated heuristic attitude', post_id=None, live_id=None)
now we can do stuff like result.id, when connected! when connection closes,
result isnt available anymore (it's detached)
'''

with Session(engine) as s:
    result = s.scalars(select(Comment))  # scalarS different then scalar!
    print(result.fetchmany(10))  # ScalarS returns an iterable!!!
    print(f'\n{result.fetchall()[-1]}')

# while .execute() (used in previous core examples) returns tuples,
# scalar/scalars return objects!


# Commiting transactions

with Session(engine) as s:
    result = s.scalar(select(Comment).where(Comment.user_id == 5))
    if result is not None:
        result.comment = 'PEI!'
        print(result.comment)
    s.commit()
