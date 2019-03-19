import pandas as pd
import tushare as ts

api = ts.pro_api('519ade7742d87ada41e0aba865dbecfadeed0a4443f6f88ff6a300a2')
cons = ts.get_apis()
df = ts.bar('000001',conn=cons, start_date='2019-03-18', end_date='2019-03-18',freq='5min')
print(df.head(20))