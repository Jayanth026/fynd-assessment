import streamlit as st

st.set_page_config(
    page_title="Fynd Feedback System",
    page_icon="🌞",
)

st.title("Fynd AI Feedback System")

st.write("Use the sidebar to navigate to:")
st.markdown("""
### 🌞 User Dashboard  
Submit reviews and get instant AI responses.  

### 🛠 Admin Dashboard  
View all submissions, summaries, and recommended actions.
""")
