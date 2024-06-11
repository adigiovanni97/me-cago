import streamlit as st
import pandas as pd
import math
from pathlib import Path
from txt_parser import parse_file
from datetime import datetime

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

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :poop: Ayudame loco
'''

# Add some spacing
''
''

from_datetime, to_datetime = st.date_input("Select a date interval", (datetime(2024, 1, 5), df['datetime'].max()))
from_datetime = datetime(from_datetime.year, from_datetime.month, from_datetime.day)
to_datetime = datetime(to_datetime.year, to_datetime.month, to_datetime.day)

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
filtered_df = df[
    (df['sender'].isin(selected_users))
    & (df['datetime'] <= to_datetime)
    & (from_datetime <= df['datetime'])
]

st.header('Time series', divider='gray')

''
''

line_chart = None

for sender in selected_users:
    filtered_sender_df = filtered_df[filtered_df.sender == sender]
    filtered_sender_df['accum'] = filtered_sender_df.reset_index().index
    if not line_chart:
        line_chart = st.line_chart(filtered_sender_df, x='datetime', y='accum', color='sender')
    else:
        line_chart.add_rows(filtered_sender_df)

