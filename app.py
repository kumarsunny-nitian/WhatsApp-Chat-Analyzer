import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader(
    "Choose a WhatsApp Chat File"
)

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    # User List
    user_list = df['user'].unique().tolist()

    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox(
        "Show Analysis W.R.T",
        user_list
    )

    start_analysis = st.sidebar.button("Show Analysis")

    if start_analysis:

        # ===================================
        # TOP STATISTICS
        # ===================================

        st.title("WhatsApp Chat Analyzer")

        num_messages, words, media, links = helper.fetch_stats(
            selected_user,
            df
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(media)

        with col4:
            st.header("Links Shared")
            st.title(links)

        # ===================================
        # MONTHLY TIMELINE
        # ===================================

        st.title("Monthly Timeline")

        timeline = helper.monthly_timeline(
            selected_user,
            df
        )

        fig, ax = plt.subplots()

        ax.plot(
            timeline['time'],
            timeline['message']
        )

        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # ===================================
        # DAILY TIMELINE
        # ===================================

        st.title("Daily Timeline")

        daily_timeline = helper.daily_timeline(
            selected_user,
            df
        )

        fig, ax = plt.subplots()

        ax.plot(
            daily_timeline['message_date'],
            daily_timeline['message']
        )

        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # ===================================
        # MOST BUSY USERS
        # ===================================

        if selected_user == 'Overall':

            st.title("Most Busy Users")

            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns(2)

            with col1:

                fig, ax = plt.subplots()

                ax.bar(
                    x.index,
                    x.values
                )

                plt.xticks(rotation='vertical')

                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # ===================================
        # WEEKLY ACTIVITY HEATMAP
        # ===================================

        st.title("Weekly Activity Heatmap")

        user_heatmap = helper.activity_heatmap(
            selected_user,
            df
        )

        fig, ax = plt.subplots(figsize=(12, 6))

        sns.heatmap(
            user_heatmap,
            ax=ax
        )

        st.pyplot(fig)

        # ===================================
        # WORD CLOUD
        # ===================================

        st.title("Word Cloud")

        df_wc = helper.create_wordcloud(
            selected_user,
            df
        )

        fig, ax = plt.subplots()

        ax.imshow(df_wc)
        ax.axis("off")

        st.pyplot(fig)

        # ===================================
        # MOST COMMON WORDS
        # ===================================

        st.title("Most Common Words")

        most_common_df = helper.most_common_words(
            selected_user,
            df
        )

        fig, ax = plt.subplots()

        ax.barh(
            most_common_df[0],
            most_common_df[1]
        )

        ax.invert_yaxis()

        st.pyplot(fig)

        # ===================================
        # EMOJI ANALYSIS
        # ===================================

        st.title("Emoji Analysis")

        emoji_df = helper.emoji_helper(
            selected_user,
            df
        )

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:

            if not emoji_df.empty:

                fig, ax = plt.subplots()

                ax.pie(
                    emoji_df[1].head(),
                    labels=emoji_df[0].head(),
                    autopct="%0.2f%%"
                )

                st.pyplot(fig)



        # ===================================
        # MONTHLY ACTIVITY MAP
        # ===================================
        
        st.title("Monthly Activity Map")
        
        monthly_activity = helper.monthly_activity_map(
            selected_user,
            df
        )
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        ax.bar(
            monthly_activity['month'],
            monthly_activity['message']
        )
        
        plt.xticks(rotation='vertical')
        
        st.pyplot(fig)