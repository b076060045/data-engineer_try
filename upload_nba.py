import pandas as pd
from sqlalchemy import create_engine, engine, text
from sqlalchemy.orm import sessionmaker
from parser_nba import parser_team
from sqlalchemy import (
    create_engine,
    engine,
    text,
    select
)
from sqlalchemy import Column, Integer, String, Float, MetaData,Table
import requests
import pymysql
import sqlalchemy
import sys
from sqlalchemy.ext.declarative import declarative_base

def build_engine():
    address = "mysql+pymysql://root:test@localhost:3306/NBA"
    engine = create_engine(address,pool_recycle = 60)
    return engine

def create_session():
    engine = build_engine()
    Session = sessionmaker(engine)
    session = Session()
    return session

def show_df_team():
    df_team = parser_team()
    return df_team

def create_table(engine):
    engine = engine
    meta = MetaData()
    s = Table(sys.argv[1],meta,
    Column('name', String(20), primary_key = True),
    Column('city', String(20)),
    Column('displayConference', String(20)),
    Column('division', String(20)),
    Column('assistsPg', Float), 
    Column('blocksPg', Float), 
    Column('fgaPg', Float),
    Column('fgmPg', Float),
    Column('foulsPg', Float),
    Column('rebsPg', Float),
    Column('stealsPg', Float),
    Column('turnoversPg', Float),
    Column('assists', Integer),
    Column('blocks', Integer),
    Column('fga', Integer),
    Column('fouls', Integer),
    Column('rebs', Integer),
    Column('steals', Integer),
    Column('turnovers', Integer))
    meta.create_all(engine)

def insert_data(df, session):
    Base = declarative_base()
    class NBA(Base):
        __tablename__ = sys.argv[1]
        name = Column(String(20), primary_key = True)
        city = Column(String(20))
        displayConference = Column(String(20))
        division = Column(String(20))
        assistsPg = Column(Float)
        blocksPg = Column(Float)
        fgaPg = Column(Float)
        fgmPg = Column(Float)
        foulsPg = Column(Float)
        rebsPg = Column(Float)
        stealsPg = Column(Float)
        turnoversPg = Column(Float)
        assists = Column(Integer)
        blocks = Column(Integer)
        fga = Column(Integer)
        fouls = Column(Integer)
        rebs = Column(Integer)
        steals = Column(Integer)
        turnovers = Column(Integer)

    query = ''

    for x in range(df.shape[0]):
        query += f"""NBA(name = df.iloc[{x}, 0],
        city = df.iloc[{x}, 1],
        displayConference = df.iloc[{x},2],
        division = df.iloc[{x}, 3],
        assistsPg = df.iloc[{x}, 4],
        blocksPg = df.iloc[{x}, 5],
        fgaPg = df.iloc[{x}, 6],
        fgmPg = df.iloc[{x}, 7],
        foulsPg = df.iloc[{x}, 8],
        rebsPg = df.iloc[{x}, 9],
        stealsPg = df.iloc[{x}, 10],
        turnoversPg = df.iloc[{x}, 11],
        assists = df.iloc[{x}, 12],
        blocks = df.iloc[{x}, 13],
        fga = df.iloc[{x}, 14],
        fouls = df.iloc[{x}, 15],
        rebs = df.iloc[{x}, 16],
        steals = df.iloc[{x}, 17],
        turnovers = df.iloc[{x}, 18]),"""

    final_query = 'session.add_all([' + query + '])'

    exec(final_query)

    session.commit()


def check_alive(engine):
    insp = sqlalchemy.inspect(engine)
    return insp.has_table(sys.argv[1])


def main():
    engine = build_engine()
    session = create_session()
    df = show_df_team()

    if check_alive(engine) == False:
        create_table(engine)
        insert_data(df, session)
    elif (check_alive(engine) == True):
        sql = text(f"select * from `{sys.argv[1]}`")
        df_exist = session.execute(sql)
        df_exist = pd.DataFrame(df_exist.mappings().all())
        if df.shape[0] != df_exist.shape[0]:
            insert_data(df, session)
        else:
            print('does not have new data')


if __name__ == '__main__':
    main()