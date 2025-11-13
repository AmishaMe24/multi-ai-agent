import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Multi AI Agent", layout="centered")
st.title("Multi AI Agent using Groq and Tavily")

system_prompt = st.text_area("Define the system prompt for the AI agents:", height=70)
selected_model = st.selectbox("Select AI Model:", options=settings.ALLOWED_MODEL_NAMES)

allowed_web_search = st.checkbox("Enable Web Search", value=False)

user_query = st.text_area("Enter your query for the AI agents:", height=150)

API_URL = "http://localhost:8000/chat"

if st.button("Ask Agent") and user_query.strip():
    payload = {
        "system_prompt": system_prompt,
        "messages" : [user_query],
        "model_name": selected_model,
        "allow_search": allowed_web_search
    }

    try:
        logger.info("Sending request to AI agent API.")
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json().get("response", "")
        logger.info("Received response from AI agent API.")
        st.subheader("AI Agent Response:")
        st.markdown(data.replace("\n", "<br>"), unsafe_allow_html=True)

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        st.error(f"An error occurred while communicating with the AI agent: {e}")

    except Exception as ex:
        logger.error(f"Unexpected error: {ex}")
        st.error(str(CustomException("An unexpected error occurred.")))