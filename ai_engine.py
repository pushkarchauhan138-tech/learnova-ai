import requests
import os

API_KEY = os.getenv("GROQ_API_KEY")

def call_ai(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    res = response.json()
    print(res)
    if "choices" in res:
        return res["choices"][0]["message"]["content"]
    else:
        return f"API Error: {res}"

def generate_roadmap(topic):
    return call_ai(f"Create a roadmap for {topic}")

def generate_explanation(topic):
    return call_ai(f"Explain {topic} in simple terms")

def generate_resources(topic):
    return call_ai(f"Give best resources to learn {topic} with links")

def chatbot_response(question):
    return call_ai(question)
