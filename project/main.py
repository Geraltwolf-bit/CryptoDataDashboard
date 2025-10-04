import pandas as pd

from fear_greed_index import get_index, preprocess_index
from inflation import get_inflation, preprocess_inflation
from stockmarket import get_stockmarket, preprocess_stockmarket
from constants import FEAR_GREED_INDEX_URL, cpi_url, api_key_cpi

ind = get_index(FEAR_GREED_INDEX_URL, limit=1)
index = preprocess_index(ind)

inf = get_inflation(cpi_url, key = api_key_cpi)
inflation = preprocess_inflation(inf)

sm = get_stockmarket()
stockmarket = preprocess_stockmarket(sm)

df = pd.merge(index, inflation, on = 'date')
df = pd.merge(df, stockmarket, on = 'date')
print(df)