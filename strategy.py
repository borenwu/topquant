# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def strategy_find_stock_1(start_time, end_time):
    engine = create_engine('mysql://root:root@127.0.0.1/stock?charset=utf8')
    sql_cmd = "SELECT * FROM stock_real_data where date >= '%s' and date <= '%s'" % (
    start_time, end_time)
    df = pd.read_sql(sql=sql_cmd, con=engine)
    # df.to_csv("2019-1-2.csv")
    # print(df)
    grouped = df.groupby(df['code'])
    code_list = []
    open_list = []
    close_list = []
    high_list = []
    low_list = []
    high_divide_low_list = []
    close_divide_open_list = []
    for name, group in grouped:
        open_value = group['open'].min()
        close_value = group['close'].max()
        high_value = group['high'].max()
        low_value = group['low'].min()
        high_divide_low_value = round((high_value / low_value), 5)
        close_divide_open_value = round((close_value / open_value), 5)

        code_list.append(name)
        open_list.append(open_value)
        close_list.append(close_value)
        high_list.append(high_value)
        low_list.append(low_value)
        high_divide_low_list.append(high_divide_low_value)
        close_divide_open_list.append(close_divide_open_value)

    result_map = {
        'code': code_list,
        'min_open': open_list,
        'max_close': close_list,
        'max_high': high_list,
        'min_low': low_list,
        'high_divide_low': high_divide_low_list,
        'close_divide_open': close_divide_open_list
    }
    columns = ['code', 'high_divide_low', 'close_divide_open', 'min_open', 'max_close', 'max_high', 'min_low']
    df = pd.DataFrame(result_map, columns=columns).sort_values(by=['high_divide_low', 'close_divide_open'],
                                                               ascending=False)
    # print(df)
    return df

if __name__ == '__main__':
    df = strategy_find_stock_1('2019-01-02 14:25','2019-01-02 14:30')
    print(df)
    df.to_csv('2019-01-02_1355-1410.csv',index=0)
