from datetime import datetime
import pandas as pd
from pathlib import Path
import re
import streamlit as st

DATETIME_RE = r"(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{2}), (?P<hour>\d{1,2}):(?P<minute>\d{2})\s(?P<meridian>[AP]M)"

MESSAGE_RE = r"(?P<datetime>\d+\/\d+\/\d{2}, \d+:\d{2}\s[A|P]M) - (?P<sender>[\w|\s]+): (?P<message>.+)"
DATA_PATH = Path(__file__).parent/'data/datos.txt'

def _parse_datetime(date_message):
  match = re.match(DATETIME_RE, date_message)
  if match:
    date_dict = match.groupdict()
    month, day, year = int(date_dict["month"]), int(date_dict["day"]), int(date_dict["year"])

    # los forros de whatsapp exportan el anio con dos digitos
    year += 2000
    hour, minute = int(date_dict["hour"]), int(date_dict["minute"])
    meridian = date_dict["meridian"]

    # Convert hour to 24-hour format based on meridian
    if meridian == "PM" and hour < 12:
        hour += 12

    # Create datetime object
    parsed_datetime = datetime(year, month, day, hour, minute)

    return parsed_datetime


def parse_file(filename=DATA_PATH):
    events = []
    with open(DATA_PATH, 'r') as file:  # 'r' for read mode
        for line in file:
            match = re.match(MESSAGE_RE, line)
            if match:
                event = {
                    "datetime": _parse_datetime(match.group("datetime")),
                    "sender": match.group("sender"),
                    "message": match.group("message")
                }

                if re.search(r"^\*?\d+\*?(\s.*)?$", event["message"]) or re.search(r"^\.$", event["message"]):
                    events.append(event)
    return pd.DataFrame(events, columns=['datetime', 'sender', 'message'])
