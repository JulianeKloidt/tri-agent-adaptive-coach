import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
# We import your hard work from the previous steps
from triathlon_coach_v1 import get_intervals_data, get_coaching_knowledge

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- PAGE SETUP ---
st.set_page_config(page_title="TriAI Coach", page_icon="🚴‍♂️")
st.title("TriAI: Adaptive Performance Director")

# --- 1. THE DATA BAR (Live API Call) ---
stats = get_intervals_data()

with st.sidebar:
    st.header("Live Athlete Data")
    if "error" not in stats:
        # The :.2f ensures the numbers are rounded to 2 decimal places
        st.metric(
            label="Fitness (CTL)", 
            value=f"{stats['ctl']:.2f}"
        )
        st.metric(
            label="Fatigue (ATL)", 
            value=f"{stats['atl']:.2f}"
        )
        st.metric(
            label="Form (TSB)", 
            value=f"{stats['tsb']:.2f}", 
            delta=f"{stats['tsb']:.2f}",
            delta_color="inverse" # Optional: red is bad for fatigue, green is good
        )
    else:
        st.error("API Connection Offline")

# --- 2. THE MEMORY (Session State) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. THE REASONING ENGINE (RAG + LLM) ---
if prompt := st.chat_input("How's the training going?"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        # A. RETRIEVE knowledge from ChromaDB
        relevant_rule = get_coaching_knowledge(prompt)
        
        # B. CONSTRUCT the context-heavy prompt
        system_instructions = f"""
        You are an expert Triathlon Coach. 
        Use the following retrieved data to inform your answer.
        
        ATHLETE STATS: {stats}
        COACHING RULE: {relevant_rule}
        
        Reference the specific stats or rules in your advice.
        """

        # C. CALL the LLM
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instructions},
                *st.session_state.messages
            ],
            stream=True # This makes the text "type out" like ChatGPT
        )
        
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})