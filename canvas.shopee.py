import pandas as pd
from config import shopee

shopee_df = pd.read_excel(shopee)

print(shopee_df.columns)