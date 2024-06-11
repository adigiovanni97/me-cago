import streamlit as st
import pandas as pd
import math
from pathlib import Path
from txt_parser import parse_file
from datetime import datetime

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP Boenas',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

#@st.cache_data
def get_msg_data():
    return parse_file()

df = get_msg_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: GDP Dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

# Add some spacing
''
''

'''Select a date interval: '''
from_datetime, to_datetime = st.date_input("Select a date interval", (df['datetime'].min(), df['datetime'].max()))
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
print(df)

# Filter the data
filtered_df = df[
    (df['sender'].isin(selected_users))
    & (df['datetime'] <= to_datetime)
    & (from_datetime <= df['datetime'])
]

st.header('Time series', divider='gray')

''
''

print(filtered_df)

st.line_chart(
    filtered_df,
    x='datetime',
    y='accum',
    color='sender',
)

''
''

''
''


# first_year = gdp_df[gdp_df['Year'] == from_year]
# last_year = gdp_df[gdp_df['Year'] == to_year]

# st.header(f'GDP in {to_year}', divider='gray')

# ''

# cols = st.columns(4)

# for i, country in enumerate(selected_countries):
#     col = cols[i % len(cols)]

#     with col:
#         first_gdp = first_year[gdp_df['Country Code'] == country]['GDP'].iat[0] / 1000000000
#         last_gdp = last_year[gdp_df['Country Code'] == country]['GDP'].iat[0] / 1000000000

#         if math.isnan(first_gdp):
#             growth = 'n/a'
#             delta_color = 'off'
#         else:
#             growth = f'{last_gdp / first_gdp:,.2f}x'
#             delta_color = 'normal'

#         st.metric(
#             label=f'{country} GDP',
#             value=f'{last_gdp:,.0f}B',
#             delta=growth,
#             delta_color=delta_color
#         )
