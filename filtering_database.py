import pandas as pd
import re
from thefuzz import fuzz, process
from functions import progress_bar

def filtering(df1, df2):

    list_judul = []
    
    progress_bar(0, len(df1['Nama Produk']))

    for i,y in enumerate(df1['Nama Produk']):
        y = re.sub(r'[-()\"#/@;:<>{}`+=~|*.!?,]',' ', y)        
        y = y.encode('ascii', 'ignore')
        y = y.decode('utf-8')
        y = y.upper()
        y = y.replace("   ", " ")
        y = y.replace("  ", " ")
        y = y.strip()
        list_judul.append(y)
        progress_bar(i+1,len(df1['Nama Produk']))
    
        
    df1_new = pd.DataFrame(columns=df1.columns)
    
    progress_bar(0, len(df2['Nama produk']))
    
    for i,x in enumerate(df2['Nama produk']):
        judul = process.extract(x, df1['Nama Produk'] , limit=1, scorer= fuzz.token_sort_ratio)
        if judul[0][1] > 75:
            idx = df1['Nama Produk'] == judul[0][0]
            rows = df1.loc[idx]
            df1_new = df1_new.append(rows, ignore_index=True)
        else:
            pass
        progress_bar(i + 1 , len(df2['Nama produk']))

    return df1_new