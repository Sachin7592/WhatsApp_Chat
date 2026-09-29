import streamlit as st
import matplotlib.pyplot as plt
import Preprocessor
import Helper
import seaborn as sns


st.sidebar.title("WhatsApp Chat Analyze")

uploaded_file = st.sidebar.file_uploader('Upload your file')
if uploaded_file is not None:
    st.title("This is WhatsApp chat Analyzer")
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = Preprocessor.Preprocessor(data)

    st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox('show analysis wrt', user_list)

    if st.sidebar.button('show analysis'):

        num_messages, words, num_media_messages, num_links = Helper.fetch_stats(selected_user,df)
        st.title('Top Statistics of WhatsApp Chat')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links shared")
            st.title(num_links)



    if selected_user == 'Overall':
        st.title("Most Busy User")
        x, new_df = Helper.most_busy_users(df)
        fig, ax = plt.subplots()





        ax.bar(x.index, x.values, color = 'red')
        st.pyplot(fig)

    most_common_df = Helper.most_common_words(selected_user, df)
    st.dataframe(most_common_df)


    fig, ax = plt.subplots()

    ax.bar(most_common_df['Most_Common_Words'], most_common_df['message_count'], color = 'orange')
    plt.xticks(rotation = 'vertical')
    st.title('Most Common Words')
    st.pyplot(fig)


    emoji_df = Helper.emoji_helper(selected_user,df)
    st.title('Emoji Analysis')

    col1, col2 = st.columns(2)

    with col1:
        if emoji_df.empty:
            st.info("No emojis found in this chat.")
        else:
            st.dataframe(emoji_df)

    with col2:
        if emoji_df.empty:
            st.info("No emojis found in this chat.")
        else:
            fig, ax = plt.subplots()
            ax.pie(
                emoji_df['Counts'].head(),
                labels=emoji_df['Emojis'].head(),
                autopct="%0.2f%%"
            )
            st.pyplot(fig)



    timeline = Helper.monthly_timeline(selected_user, df)
    st.title('Monthly Timeline Analysis')

    fig, ax = plt.subplots()

    ax.plot(timeline['time'],timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Daily timeline

    st.title('Daily Timeline Analysis')
    daily_timeline = Helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()


    ax.plot(daily_timeline['only_date'],daily_timeline['message'],
            color = 'green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.title('Activity Map')
    col1, col2 = st.columns(2)

    with col1:
        st.header("Most Busy Day")
        busy_day = Helper.week_activity_map(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values, color = 'purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        st.header('Most Busy Month')
        busy_month = Helper.month_activity_map(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,  color = 'purple')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)


    st.title('Online Activity Map')
    user_heatmap = Helper.activity_heatmap(selected_user, df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)
