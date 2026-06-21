from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Identity, Integer, MetaData, PrimaryKeyConstraint, Sequence, String, Table, UniqueConstraint

metadata = MetaData()


t_platform = Table(
    'platform', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(50), nullable=False),
    PrimaryKeyConstraint('id', name='platform_pkey')
)

t_user = Table(
    'user', metadata,
    Column('id', Integer, Sequence('users_id_seq'), primary_key=True, autoincrement=True),
    Column('username', String(30), nullable=False),
    Column('email', String(100), nullable=False),
    Column('password', String(30), nullable=False),
    PrimaryKeyConstraint('id', name='users_pkey'),
    UniqueConstraint('email', name='users_email_key'),
    UniqueConstraint('username', name='users_username_key')
)

t_live = Table(
    'live', metadata,
    Column('id', Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, autoincrement=True),
    Column('user_id', Integer, nullable=False),
    Column('platform', String(50), nullable=False),
    Column('created_at', DateTime, nullable=False),
    ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_live'),
    PrimaryKeyConstraint('id', name='live_pkey'),
    UniqueConstraint('id', name='live_id_key')
)

t_post = Table(
    'post', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, nullable=False),
    Column('post', String, nullable=False),
    Column('created_at', DateTime, nullable=False),
    ForeignKeyConstraint(['user_id'], ['user.id'], name='post_user_id_fkey'),
    PrimaryKeyConstraint('id', name='post_pkey')
)

t_comment = Table(
    'comment', metadata,
    Column('id', Integer, Sequence('comments_id_seq'), primary_key=True, autoincrement=True),
    Column('user_id', Integer, nullable=False),
    Column('comment', String(500), nullable=False),
    Column('post_id', Integer),
    Column('live_id', Integer),
    ForeignKeyConstraint(['live_id'], ['live.id'], name='fk_live_id'),
    ForeignKeyConstraint(['post_id'], ['post.id'], name='fk_post_id'),
    ForeignKeyConstraint(['user_id'], ['user.id'], name='comment_user_id_fk'),
    PrimaryKeyConstraint('id', name='comments_pkey')
)
