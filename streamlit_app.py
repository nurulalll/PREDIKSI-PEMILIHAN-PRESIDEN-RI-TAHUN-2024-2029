pip install plotly
import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from transformers import pipeline

def load_data(dataset_name):
    # Load dataset
    df = pd.read_excel(dataset_name)
    return df

def sidebar():
    st.sidebar.title('Prediksi Peilihan Presiden RI tahun 2024-2029')
    # Tambahkan ikon pada sidebar
    st.sidebar.image('https://png.pngtree.com/png-clipart/20230515/original/pngtree-election-icon-indonesian-symbol-png-image_9161556.png', width=200)
    st.sidebar.title('Menu')
    page = st.sidebar.radio("Navigate", ["Dashboard", "Text Sentiment"])
    dataset_names = {
        "Anies-CakImin": "Dataset_Anies-CakImin.xlsx",
        "Prabowo-Gibran": "Dataset_Prabowo-Gibran.xlsx",
        "Ganjar-Mahfud": "Dataset_Ganjar-Mahfud.xlsx"
    }
    selected_dataset = st.sidebar.selectbox("Select Dataset", list(dataset_names.keys()))
    df = load_data(dataset_names[selected_dataset])
    return page, df

def dashboard(df):
    st.title('Dashboard Sentimen Analisis Twitter')

    # Display dataset information
    col2, col3 = st.columns(2)
    with col2:
        st.metric("Number of rows", df.shape[0])
    with col3:
        st.metric("Number of columns", df.shape[1])

    # Display pie chart and word cloud side by side
    col1, col2 = st.columns(2)

        # Visualize sentiment using pie chart
    with col1:
        st.subheader("Sentiment Distribution")
        sentiment_counts = df['sentimen'].value_counts()
        fig = px.pie(sentiment_counts, values=sentiment_counts.values, names=sentiment_counts.index)
        fig.update_layout(width=300, height=290)  # Mengatur ukuran pie chart
        st.plotly_chart(fig)


    # Create wordcloud
    with col2:
        st.subheader("Word Cloud")
        tweet_text = ' '.join(df['Tweet'].astype(str).tolist())
        wordcloud = WordCloud(width=800, height=550, background_color ='white').generate(tweet_text)
        plt.figure(figsize=(12, 12))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt, clear_figure=False)

    # Display bar chart for top usernames
    st.subheader("Top Usernames")
    top_usernames = df['username'].value_counts().head(10)
    fig = px.bar(top_usernames, x=top_usernames.index, y=top_usernames.values,
                 labels={'x':'Username', 'y':'Count'})
    fig.update_layout(xaxis={'categoryorder':'total descending'})  # Mengurutkan username berdasarkan jumlah tweet
    st.plotly_chart(fig)



def text_sentiment():
    st.title('Text Sentiment')
    sentiment_analysis = pipeline("sentiment-analysis")
    input_text = st.text_area("Masukkan kalimat:")
    button = st.button("Analysis")

    if button:
        with st.spinner("Sedang menganalisis..."):
            result = sentiment_analysis(input_text)[0]
        st.write(f"Kalimat yang dimasukkan: {input_text}")
        st.write(f"Sentimen: {result['label']}")
        st.write(f"Confidence Score: {result['score']}")
    else:
        st.write("Ketikkan kalimat di atas dan klik tombol 'Analysis' untuk menganalisis sentimen.")


def main():
    st.set_page_config(page_title='Sentiment Analysis Dashboard')

    page, df = sidebar()
    
    if page == 'Dashboard':
        dashboard(df)
    elif page == 'Text Sentiment':
        text_sentiment()

if __name__ == "__main__":
    main()

