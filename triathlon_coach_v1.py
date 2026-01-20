import os
import json
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- 1. KNOWLEDGE RETRIEVAL ---
chroma_client = chromadb.PersistentClient(path="./db")
collection = chroma_client.get_collection(name="triathlon_rules")

def get_coaching_knowledge(query):
    results = collection.query(query_texts=[query], n_results=1)
    return results['documents'][0][0] if results['documents'] else "No specific rule found."

# --- 2. DATA RETRIEVAL (Your Robust Version) ---
def get_intervals_data():
    auth = ('API_KEY', os.getenv("INTERVALS_API_KEY"))
    athlete_id = os.getenv("INTERVALS_ATHLETE_ID")
    url = f"https://intervals.icu/api/v1/athlete/{athlete_id}/wellness"
    try:
        r = requests.get(url, auth=auth, timeout=10)
        if r.status_code == 200:
            latest = r.json()[-1]
            return {
                "ctl": latest.get('ctl', 0),
                "atl": latest.get('atl', 0),
                "tsb": (latest.get('ctl') or 0) - (latest.get('atl') or 0)
            }
        return {"error": "Could not access live data."}
    except Exception:
        return {"error": "Connection failed."}

# --- 3. THE AGENT LOGIC ---
def run_coach_agent(user_question):
    # Fetch context
    athlete_stats = get_intervals_data()
    relevant_rule = get_coaching_knowledge(user_question)
    
    system_prompt = f"""
    You are a professional Triathlon Coach. 
    Use the following context to answer the athlete's question.
    
    GROUND TRUTH RULES: {relevant_rule}
    CURRENT ATHLETE DATA: {athlete_stats}
    
    If data is missing, admit it. Always prioritize safety and the provided rules.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        temperature=0.4 # Lower temperature for more consistent, professional coaching
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    print("\n🤖 Coach is analyzing your data...")
    question = "What is my TSB?"
    print(f"\nAnswer: {run_coach_agent(question)}")