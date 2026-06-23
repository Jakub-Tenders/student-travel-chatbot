import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are Roam, a friendly AI travel assistant for students on a tight budget.
You help students find the cheapest ways to travel, sleep, and explore Europe.

Guidelines:
- Always prioritize budget-friendly options (night buses, carpooling, hostels, free activities)
- Be concise and practical, like a helpful older student who's been there
- If the user gives a budget, respect it strictly in your suggestions
- If you don't have real flight/ride data, say so honestly instead of inventing prices
- Keep responses under 150 words unless asked for more detail
"""


def get_ai_response(user_message: str, history: list = None) -> str:
    """
    Send a message to Groq's LLM and get a text response.

    Args:
        user_message: The user's latest message
        history: List of {"role": "user"/"bot", "text": "..."} from previous turns

    Returns:
        The AI's text reply as a string.
    """
    history = history or []

    # Convert our history format to OpenAI-compatible format
    # Our frontend uses role: "bot", Groq expects role: "assistant"
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in history[-10:]:  # keep last 10 messages to limit token usage
        role = "assistant" if msg["role"] == "bot" else "user"
        messages.append({"role": role, "content": msg["text"]})

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=400,
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"[llm] Groq API error: {e}")
        return "Sorry, I'm having trouble connecting right now. Try again in a moment!"


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    reply = get_ai_response("I have 50 euros and want to go somewhere from Paris this weekend")
    print(reply)