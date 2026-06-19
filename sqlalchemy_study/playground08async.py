from os import getenv

from dotenv import load_dotenv

from datetime import datetime

from sqlalchemy import ForeignKey, TIMESTAMP, func, create_engine, select

from sqlalchemy.orm import registry, Mapped, mapped_column

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



'''

ASYNC SESSION 


'''

from asyncio import run

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


async_engine = create_async_engine(DATABASE_URL)

async def main():
    async with AsyncSession(async_engine) as s:
        result = await s.scalar(select(Comment).where(Comment.user_id == 3))
        if result:
            result.comment = 'PEI!'
            print(result.comment)
            await s.commit()

run(main())