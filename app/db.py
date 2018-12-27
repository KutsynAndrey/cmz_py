from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Text, Boolean
from sqlalchemy.orm import mapper, sessionmaker


engine = create_engine('mysql+mysqlconnector://user:Dgk.cf[ytn,eleotuj@localhost/test1', echo=True)
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

problem_table = Table('problem', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('problem_title', String(50)),
                      Column('problem_body', Text),
                      Column('problem_solution', Text),
                      Column('problem_in', Text),
                      Column('problem_out', Text)
                     )


metadata.create_all(engine)


class User(object):
    def __init__(self, name, second_name, nickname, password, email, admin):
        self.name = name
        self.nickname = nickname
        self.second_name = second_name
        self.password = password
        self.email = email
        self.admin = admin

    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s', '%d' )>" % (self.name, self.second_name, self.password, self.email, self.admin)


class News(object):
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return "<new information (title --> '%s', text --> '%s'  )>" % (self.title, self.text)


class Problem(object):
    def __init__(self, title, body, problem_solution, problem_in, problem_out):
        self.problem_title = title
        self.problem_body = body
        self.problem_solution = problem_solution
        self.problem_in = problem_in
        self.problem_out = problem_out

    def __repr__ (self):
        return "Было лень писать"


mapper(User, user_table)
mapper(News, news_table)
mapper(Problem, problem_table)
