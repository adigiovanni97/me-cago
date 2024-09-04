import streamlit as st
import pandas as pd
import math
from pathlib import Path
from txt_parser import parse_file
from analytics.analytics import compute_average_per_day, filter_between_dates, compute_rolling_window
from datetime import datetime, timedelta, date

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Boenas',
    page_icon=':poop:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Data loading
@st.cache_data
def get_msg_data():
    return parse_file()

df = get_msg_data()
df['date'] = df.apply(lambda x: x['datetime'].date(), axis=1)

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :poop: Ayudame loco
'''

# Add some spacing
''
''

from_date, to_date = st.date_input("Select a date interval", (date(2024, 1, 5), df['date'].max()))
from_date = from_date - timedelta(days=1)
to_date = to_date + timedelta(days=1)

users = df['sender'].unique()

if not len(users):
    st.warning("Select at least one user")

selected_users = st.multiselect(
    'Which users would you like to view?',
    users,
    users)

''
''
''

# Filter the data
filtered_df = df[(df['sender'].isin(selected_users))]
filtered_df = filter_between_dates(filtered_df, from_date, to_date)


st.header('Time series', divider='gray')

''
''

st.subheader(':poop: count', divider = 'gray')

line_chart = None

for sender in selected_users:
    fsdf = filtered_df[filtered_df.sender == sender]
    fsdf['accum'] = fsdf.reset_index().index
    if not line_chart:
        line_chart = st.line_chart(fsdf, x='datetime', y='accum', color='sender')
    else:
        line_chart.add_rows(fsdf)


st.subheader(':poop: daily avg in a 2 week rolling window', divider = 'gray')

rolling_window_chart = None

for sender in selected_users:
    days = 14
    fsdf = filtered_df[filtered_df.sender == sender]
    fsdf = compute_rolling_window(fsdf, timedelta(days=days))
    fsdf['window_avg'] = fsdf.apply(lambda x: round(x['window']/days, 2), axis=1)
    fsdf = filter_between_dates(fsdf, fsdf['date'].min() + timedelta(days=14), fsdf['date'].max())
    if not rolling_window_chart:
        rolling_window_chart = st.line_chart(fsdf, x='datetime', y='window_avg', color='sender')
    else:
        rolling_window_chart.add_rows(fsdf)


st.header(f'Analytics per user (for selected interval)', divider='gray')

st.subheader('Daily avg (with last 2 week trend)', divider = 'gray')

cols = st.columns(2)

for i, user in enumerate(selected_users):
    col = cols[i % len(cols)]

    fsdf = filtered_df[filtered_df.sender == user]
    avg = compute_average_per_day(fsdf)
    trending_avg = compute_average_per_day(fsdf[(fsdf['datetime'] >= fsdf['datetime'].max() - timedelta(days=14))], days=14)
    delta_color = 'normal'
    if trending_avg < avg:
        trending_avg *= -1
    elif trending_avg == avg:
        delta_color = 'off'
    with col:
        st.metric(
            label=f'{user}',
            value=f'{avg:.2f}',
            delta=f'{trending_avg:.2f}',
            delta_color=delta_color
        )
