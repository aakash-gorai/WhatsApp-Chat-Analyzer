import re
import pandas as pd

def generateDataFrame(file):
    data = file.read().decode("utf-8")
    data = data.replace('\u202f', ' ')
    data = data.replace('\n', ' ')
    dt_format = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM\s|PM\s|am\s|pm\s)?-\s'
    msgs = re.split(dt_format, data)[1:]
    date_times = re.findall(dt_format, data)
    date = []
    time = []
    for dt in date_times:
        date.append(re.search('\d{1,2}/\d{1,2}/\d{2,4}', dt).group())
        time.append(re.search('\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?', dt).group())
    users = []
    message = []
    for m in msgs:
        s = re.split('([\w\W]+?):\s', m)
        if (len(s) < 3):
            users.append("Notifications")
            message.append(s[0])
        else:
            users.append(s[1])
            message.append(s[2])
    df = pd.DataFrame(list(zip(date, time, users, message)),
                      columns=["Date", "Time(U)", "User", "Message"])
    return df


def PreProcess(df, dayf):
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=dayf)
    df['Time'] = pd.to_datetime(df['Time(U)']).dt.time
    df['year'] = df['Date'].apply(lambda x: int(str(x)[:4]))
    df['month'] = df['Date'].apply(lambda x: int(str(x)[5:7]))
    df['date'] = df['Date'].apply(lambda x: int(str(x)[8:10]))
    df['day'] = df['Date'].apply(lambda x: x.day_name())
    df['hour'] = df['Time'].apply(lambda x: int(str(x)[:2]))
    df['month_name'] = df['Date'].apply(lambda x: x.month_name())
    return df
