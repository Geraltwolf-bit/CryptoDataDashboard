import pandas as pd

from fear_greed_index import get_index, figure_index
from inflation import get_inflation, figure_inflation
from stockmarket import get_stockmarket, figure_stockmarket

ind = get_index()
index = figure_index(ind)
index['date'] = index['date'].dt.date

infl = get_inflation()
inflation = figure_inflation(infl)

st = get_stockmarket()
stockmarket = figure_stockmarket(st)

df = pd.merge(index, inflation, on = 'date')
df = pd.merge(df, stockmarket, on = 'date')

print(df)