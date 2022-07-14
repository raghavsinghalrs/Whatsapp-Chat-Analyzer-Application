from urlextract import URLExtract
extract= URLExtract()
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import emoji as em

def fetch_stats(selected_user,df):

    if selected_user== 'Overall':
        # number of messages
        num_messages = df.shape[0]
        # number of words
        words=[]
        for i in df['message']:
            words.extend(i.split())
        nums_mediafiles =df[df['message'].str.contains("omitted")].shape[0]
        Links = []
        for i in df['message']:
            Links.extend(extract.find_urls(i))
        return num_messages,len(words),nums_mediafiles,len(Links)

    else:
        #number of messages
        df1 = df[df['user'] == selected_user]
        num_messages = df1.shape[0]
        #number of words
        words = []
        for i in df1['message']:
            words.extend(i.split())
        nums_mediafiles=df1[df1['message'].str.contains("omitted")].shape[0]
        Links = []
        for i in df1['message']:
            Links.extend(extract.find_urls((i)))
        return num_messages,len(words),nums_mediafiles,len(Links)

def most_busy_users(df):
    x = df.user.value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user == 'Overall':
        Another_Data = df.copy()
        Another_Data = df[df['user'] != 'notification']
        length = len(Another_Data)
        for i in range(length):
            if "omitted" in Another_Data['message'][i]:
                Another_Data.drop(i, inplace=True)
        Another_Data.reset_index(drop=True, inplace=True)
        del Another_Data['index']
        def remove_stop_words(message):
            x = []
            for i in message.lower().split():
                if i not in stop_words:
                    x.append(i)
            return "".join(x)
        wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
        Another_Data['message']=Another_Data['message'].apply(remove_stop_words)
        df_wc = wc.generate(Another_Data['message'].str.cat(sep=" "))

        return df_wc
    else:
        df1 = df[df['user'] == selected_user]
        df1.reset_index(drop=True, inplace=True)
        del df1['index']
        Another_Data = df1.copy()
        length = len(Another_Data)
        for i in range(length):
            if "omitted" in Another_Data['message'][i]:
                Another_Data.drop(i, inplace=True)

        Another_Data.reset_index(drop=True, inplace=True)
        def remove_stop_words(message):
            x = []
            for i in message.lower().split():
                if i not in stop_words:
                    x.append(i)
            return "".join(x)
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        Another_Data['message'] = Another_Data['message'].apply(remove_stop_words)
        df_wc = wc.generate(Another_Data['message'].str.cat(sep=" "))
        return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user == 'Overall':
        Another_Data = df.copy()
        Another_Data = df[df['user'] != 'notification']
        length = len(Another_Data)
        for i in range(length):
            if "omitted" in Another_Data['message'][i]:
                Another_Data.drop(i, inplace=True)
        Another_Data.reset_index(drop=True,inplace=True)
        del Another_Data['index']
        words = []
        for i in Another_Data['message']:
            for j in i.lower().split():
                if j not in stop_words:
                    words.append(j)

        frequency_words = pd.DataFrame(Counter(words).most_common(20))
        frequency_words = frequency_words[frequency_words[0] != '\u200e']

        return frequency_words

    else:
        df1 = df[df['user'] == selected_user]
        df1.reset_index(drop=True, inplace=True)
        del df1['index']
        Another_Data = df1.copy()
        length = len(Another_Data)
        for i in range(length):
            if "omitted" in Another_Data['message'][i]:
                Another_Data.drop(i, inplace=True)

        Another_Data.reset_index(drop=True,inplace=True)
        words = []

        for i in Another_Data['message']:
            for j in i.lower().split():
                if j not in stop_words:
                    words.append(j)

        frequency_words = pd.DataFrame(Counter(words).most_common(20))
        frequency_words = frequency_words[frequency_words[0] != '\u200e']
        return frequency_words

def emoji_finder(selected_user,df):

    if selected_user=="Overall":
        emojis = []
        for i in df.message:
            emojis.extend([message for message in i if message in em.UNICODE_EMOJI['en']])
        all_emojis=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
        return all_emojis

    else:
        df1 = df[df['user'] == selected_user]
        emojis = []
        for i in df1.message:
            emojis.extend([message for message in i if message in em.UNICODE_EMOJI['en']])
        all_emojis = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
        return all_emojis

def monthly_timeline(selected_user,df):

    if selected_user=="Overall":
        Timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
        time = []
        for i in range(Timeline.shape[0]):
            time.append(Timeline['month'][i] + "-" + str(Timeline['year'][i]))
        Timeline['time'] = time
        return Timeline
    else:
        df1 = df[df['user'] == selected_user]
        Timeline = df1.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
        time = []
        for i in range(Timeline.shape[0]):
            time.append(Timeline['month'][i] + "-" + str(Timeline['year'][i]))
        Timeline['time'] = time
        return Timeline

def daily_timeline(selected_user,df):

    if selected_user=='Overall':
        Daily_Timeline = df.groupby('dates').count()['message'].reset_index()
        return Daily_Timeline

    else:

        df1 = df[df['user'] == selected_user]
        Daily_Timeline = df1.groupby('dates').count()['message'].reset_index()
        return Daily_Timeline

def activity_map(selected_user,df):

    if selected_user=="Overall":
        days_df=df['day_name'].value_counts()
        return days_df
    else:
        df1 = df[df['user'] == selected_user]
        days_df = df1['day_name'].value_counts()
        return days_df
def activity_map_month(selected_user,df):
    if selected_user=="Overall":
        return df['month'].value_counts()
    else:
        df1 = df[df['user'] == selected_user]
        return df1['month'].value_counts()









