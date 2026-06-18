import re
import pandas as pd

def preprocess(data):

    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[APMapm]{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({
    'user_message': messages,
    'message_date': dates
   })

    # Fix WhatsApp special space character
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=False)
    
    # Convert string to datetime
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%m/%d/%y, %I:%M %p - '
    )
    
    users = []
    messages_list = []

    for message in df['user_message']:

        entry = re.split(r'([\w\W]+?):\s', message)

        if len(entry) >= 3:
            users.append(entry[1])
            messages_list.append(entry[2])
        else:
            users.append('group_notification')
            messages_list.append(message)

    df['user'] = users
    df['message'] = messages_list
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day



    df['day_name'] = df['message_date'].dt.day_name()

    df['hour'] = df['message_date'].dt.hour
    
    period = []
    
    for hour in df[['day_name', 'hour']]['hour']:

        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df