from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extractor = URLExtract()

def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Total Messages
    num_messages = df.shape[0]

    # Total Words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Media Messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Links
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(
        ['year', 'month_num', 'month']
    ).count()['message'].reset_index()

    time = []

    for i in range(timeline.shape[0]):
        time.append(
            timeline['month'][i] + "-" + str(timeline['year'][i])
        )

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby(df['message_date'].dt.date).count()['message'].reset_index()

    return daily_timeline

def most_busy_users(df):

    x = df['user'].value_counts().head()

    df_percent = round(
        (df['user'].value_counts() / df.shape[0]) * 100,
        2
    ).reset_index()

    df_percent.columns = ['name', 'percent']

    return x, df_percent

def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    return user_heatmap


def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():

            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(
        Counter(words).most_common(20)
    )

    return most_common_df


def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        for c in message:
            if c in emoji.EMOJI_DATA:
                emojis.append(c)

    emoji_df = pd.DataFrame(
        Counter(emojis).most_common(len(Counter(emojis)))
    )

    return emoji_df


def monthly_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    monthly_activity = df.groupby(
        ['year', 'month_num', 'month']
    ).count()['message'].reset_index()

    return monthly_activity


def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()



def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()