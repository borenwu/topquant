from downdata.GetCode import get_code

data = get_code()
data.to_csv('stk_code_full.csv',index=0)