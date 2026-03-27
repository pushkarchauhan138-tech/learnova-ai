import requests
import os

API_KEY = os.getenv("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")

def call_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo-0125",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    res_json=response.json()
    if "choices" not in res_json:
        return f"API ERROR: {res_json}"
    return response.json["choices"][0]["message"]["content"]


def generate_roadmap(topic):
    return call_ai(f"Create a roadmap for {topic}")


def generate_explanation(topic):
    return call_ai(f"Explain {topic} in simple terms")


def generate_resources(topic):
    return call_ai(f"Give best resources to learn {topic} with links")


def chatbot_response(question):
    return call_ai(question)