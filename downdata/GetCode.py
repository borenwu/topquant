import tushare as ts
from sqlalchemy import create_engine, schema, Table
from sqlalchemy.orm import sessionmaker

ts.set_token('519ade7742d87ada41e0aba865dbecfadeed0a4443f6f88ff6a300a2')
pro = ts.pro_api()

tableToWriteTo = 'stock_code_name'
engine = create_engine('mysql://root:root@127.0.0.1/stock?charset=utf8')
conn = engine.connect()

def get_code():
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry')
    data.rename(columns={'symbol':'code'}, inplace = True)
    cols = ['ts_code', 'code', 'name', 'area', 'industry']
    data = data.ix[:, cols]

    listToWrite = data.to_dict(orient='records')
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


if __name__ == '__main__':
    get_code()
