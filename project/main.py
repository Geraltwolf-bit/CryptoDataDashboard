import pandas as pd
from fear_greed_index import get_index, clean_index
from stockmarket import get_stockmarket, figure_stockmarket
from inflation import get_cpi, figure_inflation

ind = get_index()
index = clean_index(ind)

inf = get_cpi()
inflation = figure_inflation(inf)

st = get_stockmarket()
stockmarket = figure_stockmarket(st)

df = index.merge(inflation, on='date', how = 'inner')
df = df.merge(stockmarket, on='date', how = 'inner')

df