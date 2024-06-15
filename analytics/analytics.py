import pandas as pd
from datetime import datetime

def compute_average_per_day(df):
    delta = df['datetime'].max() - df['datetime'].min()
    return df.shape[0]/(delta.days)

