import tushare as ts

ts.set_token('519ade7742d87ada41e0aba865dbecfadeed0a4443f6f88ff6a300a2')
pro = ts.pro_api()

def get_code():
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    data.rename(columns={'symbol':'code'}, inplace = True)
    return data
