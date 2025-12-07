import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_PATH = "reviews.csv"

if not os.path.exists(DATA_PATH):
    pd.DataFrame(columns=["rating", "review", "ai_response"]).to_csv(DATA_PATH, index=False)

st.title("User Dashboard")
st.write("Submit your feedback and receive an AI-generated response.")

rating = st.slider("Select Rating", 1, 5, 5)
review = st.text_area("Write your review")

def generate_ai_response(review, rating):
    prompt = f"""
    The user gave a rating of {rating} and wrote the following review:

    \"\"\"{review}\"\"\"

    Write a short, friendly response thanking them for the feedback.
    """
    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=150
    )
    return response.output_text

if st.button("Submit Review"):
    if review.strip() == "":
        st.error("Please write a review before submitting.")
    else:
        ai_response = generate_ai_response(review, rating)

        df = pd.read_csv(DATA_PATH)
        df.loc[len(df)] = [rating, review, ai_response]
        df.to_csv(DATA_PATH, index=False)

        st.success("Review submitted successfully!")
        st.subheader("AI Response")
        st.write(ai_response)
