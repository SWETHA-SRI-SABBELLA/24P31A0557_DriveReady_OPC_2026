"""Drive Ready OPC 2026, Day 2: CampusBites prompts, memory and Python."""
import argparse
import functools
import json
import os


MODEL = "openai/gpt-oss-20b"
BASE_URL = "https://api.groq.com/openai/v1"
MENU = {"idli": 20, "dosa": 35, "upma": 25, "poori": 40,
        "veg fried rice": 60, "tea": 10, "coffee": 15}
FACTS = f"""ROLE:
You are the friendly customer support assistant for CampusBites.
FACTS:
Menu with prices in rupees: {json.dumps(MENU)}
Opening hours: 8 AM to 5 PM. Only vegetarian food is available.
Students can pre-order meals for campus pickup.
Bulk orders require two hours' notice."""
RULES = """RULES:
Never invent menu items, prices or offers.
Never promise delivery or exact pickup times.
Remember the customer's name and requested items using available history.
If information is unavailable, refer the customer to the canteen manager.
Do not claim an order has been placed, confirmed or prepared."""
FORMAT = "FORMAT: Reply politely in under 50 words. Use English or Telugu matching the customer."
SYSTEM = "\n\n".join((FACTS, RULES, FORMAT))
SYSTEM_NO_RULES = "\n\n".join((FACTS, FORMAT))
QUESTIONS = [
    "How much does a dosa cost?", "Do you serve chicken biryani?",
    "What are your opening hours?", "What is the cost of 3 idlis?",
    "Do you deliver food to my hostel?", "Do you offer a 50% discount?",
    "How many orders can you serve at a time?", "Can I pre-order my food?",
    "Do you serve shawarma?", "What is the combined cost of one dosa and one idli?"
]
CLASSIFIER_SYSTEM = """You are a customer message classifier for CampusBites.
Classify into order (wants food), question (wants information), or complaint (reports a problem).
Return only one word: order, question or complaint."""
EXAMPLES = [
    {"role": "user", "content": "I want two dosas."},
    {"role": "assistant", "content": "order"},
    {"role": "user", "content": "What is the price of tea?"},
    {"role": "assistant", "content": "question"},
    {"role": "user", "content": "My food is cold."},
    {"role": "assistant", "content": "complaint"},
]
CLASSIFIER_TESTS = [
    ("Pack three idlis for me.", "order"),
    ("When does the canteen open?", "question"),
    ("I received the wrong food.", "complaint"),
    ("I need five cups of coffee.", "order"),
    ("Do you serve shawarma?", "question"),
]
JSON_SYSTEM = """You are an order extraction assistant for CampusBites.
Return ONLY a valid JSON object with keys:
name (string), item (string), qty (integer), date (string), eggless (boolean).
Use null for missing information. Do not invent information.
Do not include explanations or Markdown code fences."""


def create_client():
    """Read the API key from the environment or Colab Secrets, never source code."""
    key = os.getenv("GROQ_API_KEY")
    if not key:
        try:
            from google.colab import userdata
            key = userdata.get("GROQ_API_KEY")
        except Exception:
            key = None
    if not key:
        raise SystemExit("Set GROQ_API_KEY in your environment or Colab Secrets.")
    from openai import OpenAI
    return OpenAI(api_key=key, base_url=BASE_URL)


def message(role, content):
    return {"role": role, "content": content}


def complete(client, messages, temperature=0.2):
    return client.chat.completions.create(
        model=MODEL, messages=messages, temperature=temperature
    ).choices[0].message.content


def ask(client, question, system=SYSTEM):
    return complete(client, [message("system", system), message("user", question)])


def prompt_experiment(client):
    """Assignment 1: compare the same question with and without rules."""
    question = "Can you deliver in 1 hour?"
    print("Without rules:", ask(client, question, SYSTEM_NO_RULES))
    print("With rules:", ask(client, question, SYSTEM))


def classify(client, text: str) -> str:
