# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


# import MySQLdb
#
# db = MySQLdb.connect("localhost", "root", "root", "stock", charset='utf8')
# cursor = db.cursor()
# cursor.execute("SELECT * FROM stock_real_data")
#
# results = cursor.fetchall()
#
# for row in results:
#     print(row)


def strategy_find_stock_1(start_time, end_time, trade_date):
    engine = create_engine('mysql://root:root@127.0.0.1/stock?charset=utf8')
    sql_cmd = "SELECT * FROM stock_real_data where date >= '%s' and date <= '%s'" % (start_time, end_time)
    sql_cmd_daily = "SELECT * FROM stock_daily_data where trade_date = '%s'" % (trade_date)
    sql_code_name = "SELECT * FROM stock_code_name"
    df = pd.read_sql(sql=sql_cmd, con=engine)
    daily_data = pd.read_sql(sql=sql_cmd_daily, con=engine)
    code_name = pd.read_sql(sql=sql_code_name, con=engine)
    # df.to_csv("2019-1-2.csv")
    # print(df)
    grouped = df.groupby(df['code'])
    code_list = []
    name_list = []
    industry_list = []
    open_list = []
    close_list = []
    high_list = []
    low_list = []
    interval_vol_list = []
    vol_ratio_list = []
    high_divide_low_list = []
    close_divide_open_list = []
    vol_list = []
    pct_chg_list = []

    for name, group in grouped:
        open_value = group['open'].min()
        close_value = group['close'].max()
        high_value = group['high'].max()
        low_value = group['low'].min()

        high_divide_low_value = round((high_value / low_value), 5)
        close_divide_open_value = round((close_value / open_value), 5)

        interval_vol = group['volume'].sum()
        vol_value = daily_data.loc[daily_data.code == name]['vol'].values[0]
        vol_ratio_value = round((interval_vol / vol_value), 3)

        pct_chg_value = daily_data.loc[daily_data.code == name]['pct_chg'].values[0]
        name_value = code_name.loc[code_name.code == name]['name'].values[0]
        industry_value = code_name.loc[code_name.code == name]['industry'].values[0]

        code_list.append(name)
        open_list.append(open_value)
        close_list.append(close_value)
        high_list.append(high_value)
        low_list.append(low_value)
        interval_vol_list.append(interval_vol)
        high_divide_low_list.append(high_divide_low_value)
        close_divide_open_list.append(close_divide_open_value)
        vol_list.append(vol_value)
        vol_ratio_list.append(vol_ratio_value)
        pct_chg_list.append(pct_chg_value)
        name_list.append(name_value)
        industry_list.append(industry_value)

    result_map = {
        'code': code_list,
        'name': name_list,
        'industry': industry_list,
        'min_open': open_list,
        'max_close': close_list,
        'max_high': high_list,
        'min_low': low_list,
        'high_divide_low': high_divide_low_list,
        'close_divide_open': close_divide_open_list,
        'interval_vol': interval_vol_list,
        'vol': vol_list,
        'vol_ratio': vol_ratio_list,
        'pct_chg': pct_chg_list
    }
    columns = ['code', 'name', 'industry', 'interval_vol', 'vol', 'vol_ratio', 'high_divide_low', 'close_divide_open',
               'pct_chg',
               'min_open',
               'max_close', 'max_high',
               'min_low']
    df = pd.DataFrame(result_map, columns=columns).sort_values(by=['high_divide_low', 'close_divide_open'],
                                                               ascending=False)
    # print(df)
    return df


if __name__ == '__main__':
    df = strategy_find_stock_1('2019-03-18 14:30', '2019-03-18 14:55', '20190318')
    # print(df)
    df.to_csv('2019-03-18_1430-1455.csv', index=0, encoding='utf_8_sig')
