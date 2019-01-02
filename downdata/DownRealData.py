# -*- coding: utf-8 -*-
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine, schema, Table
from sqlalchemy.orm import sessionmaker
from topdown import zsys
import arrow

tableToWriteTo = 'stock_real_data'
engine = create_engine('mysql://root:root@127.0.0.1/stock')
conn = engine.connect()


def down_min_all(rdat, finx, xtyp='5', fgIndex=False):
    '''
    根据finx列表文件，下载所有股票、指数实时数据
    【输入】
        rdat,数据文件目录
        finx:股票、指数代码文件
        xtyp (str)：k线数据模式，默认为D，日线
            D=日 W=周 M=月 ；5=5分钟 15=15分钟 ，30=30分钟 60=60分钟
        fgIndex,指数下载模式；默认为 False，股票下载模式。


    '''
    stkPool = pd.read_csv(finx, encoding='gbk');
    print(finx);
    xn9 = len(stkPool['code']);
    for i, xc in enumerate(stkPool['code']):
        code = "%06d" % xc
        print("\n", i, "/", xn9, "code,", code)
        # ---
        down_min_real010(rdat, code, xtyp, fgIndex)


def down_min_real010(rdat, xcod, xtyp='5', fgIndex=False):
    ''' 下载大盘指数数据,简版股票数据，可下载到1994年股市开市起
    【输入】
        rdat,数据文件目录
        xcod:股票、指数代码
        finx:股票、指数代码文件
        xtyp (str)：k线数据模式，默认为D，日线
            D=日 W=周 M=月 ；5=5分钟 15=15分钟 ，30=30分钟 60=60分钟
        fgIndex,指数下载模式；默认为 False，股票下载模式。



    '''
    xd = []
    xtim = arrow.now().format('YYYY-MM-DD')
    fss = rdat + xcod + '.csv';
    if fgIndex: fss = rdat + 'inx_' + xcod + '.csv';
    # print('f,',fss)
    print('\n', fss, ",", xtim);
    # -----------
    try:
        xd = ts.get_k_data(xcod, index=fgIndex, start=xtim, end=xtim, ktype=xtyp)
        # -------------
        if len(xd) > 0:
            xd = xd[zsys.ohlcDVLst]
            # print('\nxd5\n',xd.head())
            xd = xd.sort_values(['date'], ascending=True);
            xd['code'] = xcod
            xd = xd[xd.date > xtim]

            listToWrite = xd.to_dict(orient='records')
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
    except IOError:
        # print(IOError)
        pass  # skip,error

    return xd
