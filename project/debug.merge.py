import pandas as pd
from fear_greed_index import get_index, clean_index
from stockmarket import get_stockmarket, figure_stockmarket
from inflation import get_cpi, figure_inflation

ind = get_index()
print(f"get_index returned {type(ind)}")
print("\n")
index = clean_index(ind)
print(f"clean_index returned {type(index)}")
print("\n")
st = get_stockmarket()
print(f"get_stockmarket returned {type(st)}")
print("\n")
stockmarket = figure_stockmarket(st)
print(f"figure_stockmarket returned {type(stockmarket)}")
print("\n")
inf = get_cpi()
print(f"get_cpi returned {type(inf)}")
print("\n")
inflation = figure_inflation(inf)
print(f"figure_inflation returned {type(inflation)}")



