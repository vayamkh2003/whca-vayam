from urlextract import URLExtract
from wordcloud import WordCloud
import re
import pandas as pd
from collections import Counter
import emoji
extractor=URLExtract()
    
def fetch_stats(selected_user,df):

    if selected_user!="Overall":
        df=df[df['users']==selected_user]
    #number of messages
    num_messages= df.shape[0]
    #number of words
    words=[]
    for messages in df['message']:
        words.extend(messages.split())

    #number of media
    num_media=df[df['message']=='<Media omitted>\n'].shape[0]

    #number of links
    links=[]
    for messages in df['message']:
        links.extend(extractor.find_urls(messages))

    return num_messages,len(words),num_media,len(links)    

def most_active_user(df):
    x=df['users'].value_counts().head(5)
    df=round(((df['users'].value_counts())/df.shape[0])*100,2).reset_index().rename(columns={'users':'name','count':'Percentage'})
    return x,df

def word_cloud(selected_user,df):
    if selected_user!="Overall":
        df=df[df['users']==selected_user]
    
    temp=df[df['users']!='Group Notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    temp=temp[temp['message']!='null\n']#removes video call and call notifications
    temp=temp[temp['message']!='This message was deleted\n']
    temp['message'] = [messages.split("<This message was edited>\n")[0] if "<This message was edited>" in messages else messages for messages in temp['message']]

    
    f=open('stop_hinglish.txt','r',encoding="utf-8")
    stopwords=f.read()

    def remove_stopword(message):#removing stopwords
        y=[]
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white',)
    temp['message']=temp['message'].apply(remove_stopword)    
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def most_common_word(selected_user,df):
    if selected_user!="Overall":
        df=df[df['users']==selected_user]
    temp=df[df['users']!='Group Notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    temp=temp[temp['message']!='null\n']
    temp=temp[temp['message']!='This message was deleted\n']
    temp['message'] = [messages.split("<This message was edited>\n")[0] if "<This message was edited>" in messages else messages for messages in temp['message']]
    
    f=open('stop_hinglish.txt','r',encoding="utf-8")
    stopwords=f.read()
    
    words=[]
    for messages in temp['message']:
        for word in messages.lower().split():
            if word not in stopwords:
                words.append(word)
    df_common_words=pd.DataFrame(Counter(words).most_common(20),columns=['Word','Count'])
    
    return df_common_words

def emojis(selected_user,df):
    if selected_user!="Overall":
        df=df[df['users']==selected_user]
    emojis=[]
    for messages in df['message']:
        emojis.extend(c for c in messages if c in emoji.EMOJI_DATA)
    df_emoji=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),columns=['Emoji','Count'])
    return df_emoji

def monthly_Timeline(selected_user,df):
    if selected_user!="Overall":
        df=df[df['users']==selected_user]
    

    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    
    timeline['time']=time

    return timeline
def daily_Timeline(selected_user,df):
    if selected_user!="Overall":
        df=df[df['users']==selected_user]
    
    
    daily_timeline=df.groupby('o_date')['message'].count().reset_index()
    return daily_timeline

def weekly_Activity(selected_user,df):
    if selected_user!="Overall":
        df=df[df['users']==selected_user]
    
    weekly_activity=df['day_name'].value_counts().reset_index()
    weekly_activity.columns=['day','count']
    return weekly_activity

def monthly_Activity(selected_user,df):
    if selected_user!="Overall":
        df=df[df['users']==selected_user]

    monthly_activity=df['month'].value_counts().reset_index()
    monthly_activity.columns=['month','count']
    return monthly_activity

def activity_Heatmap(selected_user,df):
    if selected_user!="Overall":
        df=df[df['users']==selected_user]
    activity_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activity_heatmap