'''

DB MODEL GENERATED WITH sqlacodegen!

terminal:
sqlacodegen <database_url> 
    # echoes code in terminal
    # default: declarative ORM

sqlacodegen --generator dataclasses <database_url>
    # using --generator <dataclasses> generates ORM dataclass-based models 
    # (see models_dataclass.py module)
    # --generator can also be used to generate SQLAlchemy core Tables : --generator tables

sqlacodegen <database_url> > module_name.py
    # generates module with code!     

'''


from typing import Optional
import datetime

from sqlalchemy import DateTime, ForeignKeyConstraint, Identity, Integer, PrimaryKeyConstraint, Sequence, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Platform(Base):
    __tablename__ = 'platform'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='platform_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('username', name='users_username_key')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('users_id_seq'), primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(30), nullable=False)

    live: Mapped[list['Live']] = relationship('Live', back_populates='user')
    post: Mapped[list['Post']] = relationship('Post', back_populates='user')
    comment: Mapped[list['Comment']] = relationship('Comment', back_populates='user')


class Live(Base):
    __tablename__ = 'live'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_live'),
        PrimaryKeyConstraint('id', name='live_pkey'),
        UniqueConstraint('id', name='live_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='live')
    comment: Mapped[list['Comment']] = relationship('Comment', back_populates='live')


class Post(Base):
    __tablename__ = 'post'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user.id'], name='post_user_id_fkey'),
        PrimaryKeyConstraint('id', name='post_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    post: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='post')
    comment: Mapped[list['Comment']] = relationship('Comment', back_populates='post')


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = (
        ForeignKeyConstraint(['live_id'], ['live.id'], name='fk_live_id'),
        ForeignKeyConstraint(['post_id'], ['post.id'], name='fk_post_id'),
        ForeignKeyConstraint(['user_id'], ['user.id'], name='comment_user_id_fk'),
        PrimaryKeyConstraint('id', name='comments_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('comments_id_seq'), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(String(500), nullable=False)
    post_id: Mapped[Optional[int]] = mapped_column(Integer)
    live_id: Mapped[Optional[int]] = mapped_column(Integer)

    live: Mapped[Optional['Live']] = relationship('Live', back_populates='comment')
    post: Mapped[Optional['Post']] = relationship('Post', back_populates='comment')
    user: Mapped['User'] = relationship('User', back_populates='comment')
