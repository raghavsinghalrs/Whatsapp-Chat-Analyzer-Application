import pandas as pd
import regex as re


def preprocess(data):
    pattern = '\[\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}:\d{2}\s[AP]M\]\s'

    messages = re.split(pattern, data)[2:]

    dates = re.findall(pattern, data)[1:]

    df = pd.DataFrame({'user_message': messages, "message_date": dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format="[%d/%m/%y, %I:%M:%S %p] ")

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['dates'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute
    df['seconds'] = df['date'].dt.second
    df.drop(df[df['message'] == ""].index, inplace=True)
    df.reset_index(inplace=True)

    return df