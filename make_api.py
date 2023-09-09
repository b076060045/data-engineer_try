import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine, engine, text
from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy import (
    create_engine,
    engine,
    text,
    select
)
app = FastAPI()

def get_mysql_nba_conn():
    address = "mysql+pymysql://root:test@localhost:3306/NBA"
    engine = create_engine(address,pool_recycle = 60)
    Session = sessionmaker(engine)
    session = Session()
    #connect = engine.connect()
    return session

@app.get("/")
def first_page():
    return {'Hello':'This is the page of NBA STATS'}

@app.get("/{select_year}")
def get_data(select_year):
    session = get_mysql_nba_conn()
    sql = text(f"select * from `{select_year}`")
    df = session.execute(sql)
    df = pd.DataFrame(df.mappings().all())
    df_dict = df.to_dict('records')
    session.commit()
    print(df_dict)
    return {'data':df_dict}

@app.get("/{select_year}/{item}")
def get_data(select_year, item):
    session = get_mysql_nba_conn()
    sql = text(f"select * from `player_{select_year}` order by {item} desc")
    df = session.execute(sql)
    df = pd.DataFrame(df.mappings().all())
    df_dict = df.to_dict('records')
    session.commit()
    return {'data':df_dict}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)
