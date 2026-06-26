"""
Benchmark script for the "GenAI performance" grading criterion.

Unlike a generic prompt test, this uses our ACTUAL mock data
(flights, rides, hostels) run through the SAME prompt_builder.py
that the real /api/chat endpoint uses. This shows how each model
handles real app data, not just general travel chit-chat.

Run with: python benchmark.py
"""

import os
import time
from groq import Groq
from dotenv import load_dotenv

from services.sky_scrapper import search_one_way
from services.blablacar import search_rides
from services.hostels import search_hostels
from utils.prompt_builder import build_travel_context

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

# Models to compare — both available directly through Groq, no extra signup needed
MODELS = [
    "llama-3.1-8b-instant",     # current production model — fast, small
    "llama-3.3-70b-versatile",  # larger model — slower, potentially more detailed
]

# Real test scenarios using our actual mock data pipeline
TEST_CASES = [
    {
        "user_message": "I have 50 euros, what are my cheapest options to Berlin?",
        "origin": "Paris",
        "destination": "Berlin",
        "date": "2026-09-15",
    },
    {
        "user_message": "Find me a budget weekend trip to Amsterdam",
        "origin": "Paris",
        "destination": "Amsterdam",
        "date": "2026-09-20",
    },
    {
        "user_message": "What's the cheapest hostel option and how do I get there?",
        "origin": "Lyon",
        "destination": "Barcelona",
        "date": "2026-10-01",
    },
]


def build_context_for_case(case):
    """Pull real mock data from our services, exactly like routes/chat.py does."""
    flights = search_one_way(case["origin"], case["destination"], case["date"])
    rides = search_rides(case["origin"], case["destination"], case["date"])
    hostels = search_hostels(case["destination"])
    return build_travel_context(flights=flights, rides=rides, hostels=hostels)


def run_benchmark():
    results = []

    for model in MODELS:
        print(f"\n{'='*70}\nMODEL: {model}\n{'='*70}")

        for case in TEST_CASES:
            context = build_context_for_case(case)

            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            if context:
                messages.append({"role": "user", "content": context})
                messages.append({"role": "assistant", "content": "Got it, I'll use that data in my response."})
            messages.append({"role": "user", "content": case["user_message"]})

            start = time.time()
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=300,
                )
                elapsed = round(time.time() - start, 2)
                reply = response.choices[0].message.content
                tokens = response.usage.total_tokens if response.usage else "?"

                print(f"\nUser: {case['user_message']}")
                print(f"Route: {case['origin']} -> {case['destination']} on {case['date']}")
                print(f"Time: {elapsed}s | Tokens: {tokens}")
                print(f"Reply: {reply}\n{'-'*70}")

                results.append({
                    "model": model,
                    "user_message": case["user_message"],
                    "time_seconds": elapsed,
                    "tokens": tokens,
                    "reply": reply,
                })

            except Exception as e:
                print(f"Error with {model} on '{case['user_message']}': {e}")

    return results


if __name__ == "__main__":
    run_benchmark()