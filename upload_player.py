import pandas as pd
from sqlalchemy import create_engine, engine, text
from sqlalchemy.orm import sessionmaker
from parser_player import parser_player
from sqlalchemy import (
    create_engine,
    engine,
    text,
    select
)
from sqlalchemy import Column, Integer, String, Float, MetaData,Table
from sqlalchemy.dialects.mysql import LONGTEXT
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
    df_team = parser_player(sys.argv[1])
    return df_team

def create_table(engine):
    engine = engine
    meta = MetaData()
    s = Table(f'player_{sys.argv[1]}', meta,
        Column('name', String(200), primary_key = True),
        Column('country', String(200)),
        Column('pointsPg', Float),
        Column('assistsPg', Float),
        Column('blocksPg', Float),
        Column('efficiency', Float),
        Column('rebsPg', Float),
        Column('stealsPg', Float),
        Column('turnoversPg', Float),
        Column('assists', Integer),
        Column('blocks', Integer),
        Column('rebs', Integer),
        Column('steals', Integer),
        Column('turnovers', Integer))
    meta.create_all(engine)

def insert_data(df, session):
    Base = declarative_base()
    class NBA(Base):
        __tablename__ = f'player_{sys.argv[1]}'
        name = Column(String(200), primary_key = True)
        country = Column(String(200))
        pointsPg = Column(Float)
        assistsPg = Column(Float)
        blocksPg = Column(Float)
        efficiency = Column(Float)
        rebsPg = Column(Float)
        stealsPg = Column(Float)
        turnoversPg = Column(Float)
        assists = Column(Integer)
        blocks = Column(Integer)
        rebs = Column(Integer)
        steals = Column(Integer)
        turnovers = Column(Integer)
    
    query = ''

    for x in range(df.shape[0]):
        query +=  f"""NBA(name = df.iloc[{x}, 0],
        country = df.iloc[{x}, 1],
        pointsPg = df.iloc[{x}, 2],
        assistsPg = df.iloc[{x}, 3],
        blocksPg = df.iloc[{x}, 4],
        efficiency = df.iloc[{x}, 5],
        rebsPg = df.iloc[{x}, 6],
        stealsPg = df.iloc[{x}, 7],
        turnoversPg = df.iloc[{x}, 8],
        assists = df.iloc[{x}, 9],
        blocks = df.iloc[{x}, 10],
        rebs = df.iloc[{x}, 11],
        steals = df.iloc[{x}, 12],
        turnovers = df.iloc[{x}, 13]),"""
    
    final_query = 'session.add_all([' + query + '])'

    exec(final_query)

    session.commit()

def check_alive(engine):
    insp = sqlalchemy.inspect(engine)
    return insp.has_table(f'player_{sys.argv[1]}')

def main():
    engine = build_engine()
    session = create_session()
    df = show_df_team()

    if check_alive(engine) == False:
        create_table(engine)
        insert_data(df, session)
    elif (check_alive(engine) == True):
        sql = text(f"select * from `player_{sys.argv[1]}`")
        df_exist = session.execute(sql)
        df_exist = pd.DataFrame(df_exist.mappings().all())
        if df.shape[0] != df_exist.shape[0]:
            insert_data(df, session)
        else:
            print('does not have new data')

    

if __name__ == '__main__':
    main()