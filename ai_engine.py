import requests
import os

# Configure your API key here or set as environment variable
API_KEY = os.getenv("GROQ_API_KEY")

def call_ai(prompt):
    if not API_KEY:
        return "GROQ_KEY not set"
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    res = response.json()
    if "choices" in res:
        return res["choices"][0]["message"]["content"]
    else:
        return f"API Error: {res}"

def generate_roadmap(topic: str) -> str:
    prompt = f"""
    Create a clear, structured learning roadmap for: "{topic}".
    
    Format it as numbered stages with bold titles. Be practical and progressive.
    Cover beginner to advanced. Keep it under 300 words.
    Use markdown formatting.
    """
    try:
        return call_ai(prompt)
    except Exception as e:
        return f"Error generating roadmap: {str(e)}"


def generate_explanation(topic: str) -> str:
    prompt = f"""
    Give a clear, engaging explanation of "{topic}" for a motivated learner.
    
    Cover:
    - What it is
    - Why it matters
    - Key concepts and real-world use cases
    
    Use simple language. Keep it under 250 words. Use markdown formatting.
    """
    try:
        return call_ai(prompt)
    except Exception as e:
        return f"Error generating explanation: {str(e)}"


def generate_resources(topic: str) -> str:
    prompt = f"""
    List 5-6 top learning resources for "{topic}".
    
    Include a mix of:
    - Free online courses (Coursera, edX, YouTube)
    - Books (beginner and advanced)
    - Websites and documentation
    - Paid courses if highly recommended
    
    Format as a clean markdown list with brief descriptions for each.
    Keep it under 200 words.
    """
    try:
        return call_ai(prompt)
    except Exception as e:
        return f"Error generating resources: {str(e)}"


def chatbot_response(question: str) -> str:
    prompt = f"""
    You are Learnova, an expert AI learning mentor. A student asks:
    
    "{question}"
    
    Give a helpful, concise, and encouraging response. Max 150 words.
    Use markdown formatting where helpful.
    """
    try:
        return call_ai(prompt)
    except Exception as e:
        return f"Sorry, I couldn't respond right now. Error: {str(e)}"
