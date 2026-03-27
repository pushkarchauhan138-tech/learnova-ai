import requests

API_KEY = "sk-or-v1-9a5561e9c1584d1aff02301c6ce7b38d86bb0e002cbf161220bf908cf2d6b3bdE"

def call_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        res_json = response.json()

        # DEBUG (optional)
        print(res_json)

        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        else:
            return f"API Error: {res_json}"

    except Exception as e:
        return f"Error: {str(e)}"


def generate_roadmap(topic):
    return call_ai(f"Create a roadmap for {topic}")

def generate_explanation(topic):
    return call_ai(f"Explain {topic} in simple terms")

def generate_resources(topic):
    return call_ai(f"Give best learning resources for {topic}")

def chatbot_response(q):
    return call_ai(q)