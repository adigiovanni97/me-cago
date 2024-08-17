import pandas as pd
from datetime import timedelta

def compute_average_per_day(df, days=0):
    if days == 0:
        days = (df['datetime'].max() - df['datetime'].min()).days
    return round(df.shape[0]/days, 2)

def filter_between_dates(df, d_from, d_to):
    return df[(df['date'] >= d_from) & (df['date'] <= d_to)]

def compute_rolling_window(df, t_delta=timedelta(days=14)):
    df['window'] = df.apply(lambda x: count_in_prev_window(df, x['date'], t_delta), axis=1)
    return df

def count_in_prev_window(df, date, t_delta):
    return filter_between_dates(df, date - t_delta, date).shape[0]