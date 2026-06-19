import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def get_knowledge(query):

    if "api" in query.lower():
        with open("data/api_troubleshooting.txt", "r") as file:
            return file.read()

    elif "billing" in query.lower():
        with open("data/billing_policy.txt", "r") as file:
            return file.read()

    elif "password" in query.lower():
        with open("data/password_reset.txt", "r") as file:
            return file.read()

    return "No relevant document found."
def check_escalation(query):

    text = query.lower()

    if "legal" in text or "lawsuit" in text or "refund not received" in text:
        return True

    return False

def detect_persona(query):
    text = query.lower()

    if "api" in text or "error" in text or "token" in text:
        return "Technical Expert"
    elif "frustrated" in text or "angry" in text or "terrible" in text:
        return "Frustrated User"
    else:
        return "Business Executive"

st.title("Persona-Adaptive Customer Support Agent")

user_query = st.text_area("Enter your query")

if st.button("Submit"):

    persona = detect_persona(user_query)

    st.subheader("Detected Persona")
    st.success(persona)
    knowledge = get_knowledge(user_query)

    st.subheader("Retrieved Knowledge")
    st.info(knowledge)

    knowledge = get_knowledge(user_query)

    prompt = f"""
    User Persona: {persona}

    Knowledge Base Information:
    {knowledge}

    User Query:
    {user_query}

    Generate a customer support response using the knowledge base information.
    """
    st.subheader("AI Response")
try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    st.subheader("AI Response")
    st.write(response.text)

except Exception as e:
    st.error(f"Error: {e}")
escalate = check_escalation(user_query)

st.subheader("Escalation Status")
if escalate:
    
    st.subheader("Human Handoff Summary")

    summary = f"""
    User Query: {user_query}

    Detected Persona: {persona}

    Escalation Reason:
    Legal issue or refund dispute detected.
    """

    st.info(summary)
    st.error("Escalation Required")
else:
    st.success("No Escalation Required")