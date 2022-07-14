import matplotlib.pyplot as plt
import streamlit as st
import preprocessor
import helper

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_files = st.sidebar.file_uploader("Choose a file")
if uploaded_files is not None:
    bytes_data = uploaded_files.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    #st.dataframe(df)
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Choose an option", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, nums_mediafiles, Links= helper.fetch_stats(selected_user, df)
        col1,col2,col3 = st.columns(3)
        with col1:
            st.title("")
        with col2:
            st.title("Chat Statistics")
        with col3:
            st.title("")
        st.title("")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(nums_mediafiles)
        with col4:
            st.header('Links Shared')
            st.title(Links)
        st.title("")

        #monthly timeline
        st.title("Monthly Timeline")
        Timeline = helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(Timeline['time'], Timeline['message'],"b-.")
        plt.xticks(rotation="vertical")
        plt.ylabel("Number of messages")
        st.pyplot(fig)

        st.title("")

        #daily timeline
        st.title("Daily Timeline")
        Daily_Timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(Daily_Timeline['dates'], Daily_Timeline['message'], "g--")
        plt.xticks(rotation="vertical")
        plt.ylabel("Number of messages")
        st.pyplot(fig)
        st.title("")

        #timeline based on days
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            days_df=helper.activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(days_df.index,days_df.values,color='magenta')
            plt.xticks(rotation=90)
            plt.ylabel("Number of messages")
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            month_df = helper.activity_map_month(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(month_df.index, month_df.values,color='black')
            plt.xticks(rotation=90)
            plt.ylabel("Number of messages")
            st.pyplot(fig)



        st.title("")
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, new_df= helper.most_busy_users(df)
            fig,ax = plt.subplots()
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation=90)
                plt.ylabel("Number of Messages wrt user")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
    st.title("")
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.title("WordCloud")
    st.pyplot(fig)
    st.title("")
    frequency_words = helper.most_common_words(selected_user,df)
    fig,ax = plt.subplots()
    ax.barh(frequency_words[0],frequency_words[1])
    st.title("Most Common Words")
    st.pyplot(fig)
    st.title("")
    all_emojis = helper.emoji_finder(selected_user,df)
    st.title("Emojis Analysis")
    col1,col2 = st.columns(2)
    with col1:
        st.dataframe(all_emojis)
    with col2:
        fig,ax = plt.subplots()
        ax.pie(all_emojis[1].head(),labels=all_emojis[0].head(),autopct="%0.2f")
        st.pyplot(fig)





