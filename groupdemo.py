# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sqlalchemy import create_engine




engine = create_engine('mysql://root:root@127.0.0.1/stock?charset=utf8')
sql_cmd = "SELECT * FROM real_data"
df = pd.read_sql(sql=sql_cmd, con=engine)
# print(df)
grouped = df.groupby(df['code'])
for name,group in grouped:
    end = group.iloc[[-1]]['close'].values[0]
    begin = group.iloc[[0]]['close'].values[0]
    # print(end)
    # print(begin)
    # print(end - begin)
    percentage = (end - begin) / begin
    print('\ncode: '+name)
    print('percentage: '+ str(round(percentage,2)))
