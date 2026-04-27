import google.generativeai as genai
import os

# Configure your API key here or set as environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_roadmap(topic: str) -> str:
    prompt = f"""
    Create a clear, structured learning roadmap for: "{topic}".
    
    Format it as numbered stages with bold titles. Be practical and progressive.
    Cover beginner to advanced. Keep it under 300 words.
    Use markdown formatting.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
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
        response = model.generate_content(prompt)
        return response.text
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
        response = model.generate_content(prompt)
        return response.text
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
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't respond right now. Error: {str(e)}"
