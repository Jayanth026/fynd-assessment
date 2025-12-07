import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_PATH = "reviews.csv"

st.title("🛠 Admin Dashboard")
st.write("Monitor user feedback, summaries, and recommended actions.")

if not os.path.exists(DATA_PATH):
    st.warning("No reviews submitted yet.")
    st.stop()

df = pd.read_csv(DATA_PATH)

if df.empty:
    st.warning("No reviews submitted yet.")
    st.stop()

st.subheader("All Submissions")
st.dataframe(df)

st.subheader("Analytics")
st.write(f"Average Rating: **{df['rating'].mean():.2f}**")

rating_counts = df['rating'].value_counts().sort_index()
st.bar_chart(rating_counts)

def summarize_and_recommend(review):
    prompt = f"""
    A user wrote the following review:

    \"\"\"{review}\"\"\"

    Provide:
    1. A 1-sentence summary
    2. Recommended business action (1–2 sentences)

    Return in plain text.
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=200
    )
    return response.output_text

st.subheader("AI Insights")

selected_index = st.selectbox("Choose a review index", df.index)
selected_review = df.loc[selected_index, "review"]

if st.button("Generate Insights"):
    insights = summarize_and_recommend(selected_review)
    st.write(insights)
