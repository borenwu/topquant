# -*- coding: utf-8 -*-
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine, schema, Table
from sqlalchemy.orm import sessionmaker
from topdown import zsys
import arrow

ts.set_token('519ade7742d87ada41e0aba865dbecfadeed0a4443f6f88ff6a300a2')
pro = ts.pro_api()

tableToWriteTo = 'stock_daily_data'
engine = create_engine('mysql://root:root@127.0.0.1/stock')
conn = engine.connect()


def down_daily_all(trade_date):
    df = pro.daily(trade_date=trade_date)
    df['code'] = df['ts_code'].str.split('.', expand=True)[0]
    cols = ['trade_date', 'ts_code', 'code', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol',
            'amount']
    df = df.ix[:, cols]
    listToWrite = df.to_dict(orient='records')
    metadata = schema.MetaData(bind=engine, reflect=True)
    table = Table(tableToWriteTo, metadata, autoload=True)

    # Open the session
    Session = sessionmaker(bind=engine)
    session = Session()
    # xd.to_sql('stock_real_data', engine, if_exists='append')
    # xd.to_csv(fss, index=False, encoding='gbk')
    # Inser the dataframe into the database in one bulk
    conn.execute(table.insert(), listToWrite)

    # Commit the changes
    session.commit()

    # Close the session
    session.close()

    return df


if __name__ == '__main__':
    df = down_daily_all('20190102')
    print(df)
