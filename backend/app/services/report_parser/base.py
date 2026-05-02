import pandas as pd

def normalize_col(c:str)->str: return str(c).strip().lower().replace('ё','е').replace('\n',' ')
def to_num(v):
    if v is None:return None
    s=str(v).replace('₽','').replace(' ','').replace(',','.')
    try:return float(s)
    except:return None

def load_df(path:str): return pd.read_csv(path) if path.lower().endswith('.csv') else pd.read_excel(path)
