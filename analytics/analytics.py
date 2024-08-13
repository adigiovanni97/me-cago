import pandas as pd
from datetime import datetime

def compute_average_per_day(df, days=0):
    if days == 0:
        days = (df['datetime'].max() - df['datetime'].min()).days
    return round(df.shape[0]/days, 2)
