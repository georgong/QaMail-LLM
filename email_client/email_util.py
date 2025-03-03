
import re
from datetime import datetime
from tzlocal import get_localzone
import pytz

def str2datetime(date_string):
    # Use regex to remove any extra characters after the timezone offset
    cleaned_date_string = re.sub(r' \([^)]+\)$', '', date_string)

    # Define regex patterns for both formats
    pattern_with_day = r'^([A-Za-z]{3}), (\d{1,2} [A-Za-z]{3} \d{4} \d{2}:\d{2}:\d{2} [+-]\d{4})'
    pattern_without_day = r'^(\d{1,2} [A-Za-z]{3} \d{4} \d{2}:\d{2}:\d{2} [+-]\d{4})'

    # Check if the cleaned input string matches the pattern with day
    match_with_day = re.match(pattern_with_day, cleaned_date_string)
    if match_with_day:
        day_of_week = match_with_day.group(1)
        date_part = match_with_day.group(2)
    else:
        # Check if the cleaned input string matches the pattern without day
        match_without_day = re.match(pattern_without_day, cleaned_date_string)
        if match_without_day:
            date_part = match_without_day.group(1)
            # Parse the date part to get the day of the week
            temp_date_object = datetime.strptime(date_part, '%d %b %Y %H:%M:%S %z')
            day_of_week = temp_date_object.strftime('%A')
        else:
            print(match_without_day)
            print(date_string)
            return date_string
            #raise ValueError("Invalid date format")

    # Parse the date part as UTC
    utc_date_object = datetime.strptime(date_part, '%d %b %Y %H:%M:%S %z')
    utc_date_object = utc_date_object.replace(tzinfo=pytz.utc)

    # Convert UTC to local
    tz = get_localzone()
    #pst_date_object = utc_date_object
    pst_date_object = utc_date_object.replace(tzinfo=tz)
    # Extract components
    year = pst_date_object.strftime('%Y')
    month = pst_date_object.strftime('%m')
    day = pst_date_object.strftime('%d')
    hours = pst_date_object.strftime('%H')
    minutes = pst_date_object.strftime('%M')
    seconds = pst_date_object.strftime('%S')
    timezone = pst_date_object.strftime('%z')

    # Format the date string
    formatted_date = f"{year}/{month}/{day} {hours}:{minutes}:{seconds}"
    dt = datetime.strptime(formatted_date, "%Y/%m/%d %H:%M:%S")
    return dt
    
        
def timestamp2str(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    formatted_date = dt.strftime("%Y/%m/%d %H:%M:%S")
    return formatted_date

def date2dt(formatted_date):
    dt = datetime.strptime(formatted_date, "%Y-%m-%d")
    return dt


    
# $ pip install pytz #pytz-2025.1
# $ pip install tzlocal #tzlocal-5.2
if __name__ == "__main__":
    print(str2datetime('Wed, 05 Feb 2025 17:01:25 -0500').timestamp())