from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Text, Boolean
from sqlalchemy.orm import mapper, sessionmaker


engine = create_engine('<your database`s url>', echo=True)
metadata = MetaData()
Session = sessionmaker(bind=engine)

user_table = Table('users', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(50)),
                   Column('second_name', String(50)),
                   Column('nickname', String(50)),
                   Column('password', String(50)),
                   Column('email', String(50)),
                   Column('admin', Boolean)
                   )

news_table = Table('news', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('title', String(50)),
                   Column('text', Text)
                   )


metadata.create_all(engine)


class User(object):
    def __init__(self, name, second_name, nickname, password, email, admin):
        self.name = name
        self.nickname = nickname
        self.second_name = second_name
        self.password = password
        self.email = email
        self.admin = False

    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s', '%d' )>" % (self.name, self.second_name, self.password, self.email, self.admin)


class News(object):
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return "<new information (title --> '%s', text --> '%s'  )>" % (self.title, self.text)


mapper(User, user_table)
mapper(News, news_table)
