import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import wordcloud
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    # st.text(data)
    #data to dataframe named df
    df=preprocessor.preprocess(data)
    
    # st.dataframe(df)

    users_list=df['users'].unique().tolist()
    users_list.remove('Group Notification')
    users_list.sort()
    users_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("Show me analysis wrt ",users_list)
    
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media,num_links=helper.fetch_stats(selected_user,df)
        st.title("Statistics {Cause we need it :)}")

        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(num_media)
        with col4:
            st.header("Total Links")
            st.title(num_links)
        
        #monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_Timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='orange')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_Timeline(selected_user,df)
        fig,ax=plt.subplots(figsize=(18,10))
        ax.plot(daily_timeline['o_date'],daily_timeline['message'],color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)
        
        #weekly activity map
        st.title("Weekly Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day=helper.weekly_Activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day['day'], busy_day['count'], color='black')
            plt.xticks(rotation=90)
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month=helper.monthly_Activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month['month'], busy_month['count'], color='gold')
            plt.xticks(rotation=90)
            st.pyplot(fig)
        #activity heatmap
        st.title("Weekly Activity Heatmap")
        activity_heatmap=helper.activity_Heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(activity_heatmap)
        st.pyplot(fig)

        #most active user
        if selected_user=='Overall':
            col1,col2=st.columns(2)
            most_activeuser,df_percent=helper.most_active_user(df)
        
            fig,ax=plt.subplots()
            
            with col1:
                st.header("Most Active User")
                ax.bar(most_activeuser.index,most_activeuser.values,color='red')
                
                st.pyplot(fig)
            with col2:
                st.header("Percentage of Messages")
                st.dataframe(df_percent)   
        #wordcloud
        st.title("Word Cloud")
        df_wc=helper.word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title("Most Common Words")
        col1,col2=st.columns(2)
        df_common_words=helper.most_common_word(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(df_common_words['Word'],df_common_words['Count'])

        plt.xticks(rotation=90)
        with col1:
            st.pyplot(fig)
        with col2:
            st.dataframe(df_common_words,height=300)

        #emojis analysis
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)
        df_emojis=helper.emojis(selected_user,df)
        with col1:
            st.dataframe(df_emojis)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(df_emojis['Count'].head(5),labels=df_emojis['Emoji'].head(5),autopct='%0.2f%%')
            st.pyplot(fig)
        
            