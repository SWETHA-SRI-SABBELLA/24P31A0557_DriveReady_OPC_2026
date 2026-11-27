"""Day 1 - CampusBites LLM fundamentals and practical assignments.

The menu and policies describe a fictional campus canteen for learning.
Set GROQ_API_KEY as an environment variable or a Google Colab secret.
Run: python task.py --help
"""

import argparse
import os

MODEL = "openai/gpt-oss-20b"
BASE_URL = "https://api.groq.com/openai/v1"

SYSTEM = """
ROLE:
You are the customer support assistant for CampusBites.

FACTS:
1. Menu: Idli Rs 20, Dosa Rs 35, Upma Rs 25,
   Poori Rs 40, Veg Fried Rice Rs 60,
   Tea Rs 10 and Coffee Rs 15.
2. We are open from 8 AM to 5 PM.
3. We serve only vegetarian food.
4. Students can pre-order meals for campus pickup.
5. Bulk orders require two hours' notice.

RULES:
1. Never invent menu items, prices or offers.
2. Never promise an exact pickup time.
3. If information is unavailable, say
   "I'll check with the canteen manager."

FORMAT:
Reply politely in under 50 words.
Use English or Telugu based on the customer's language.
"""

# Remove only the FACTS section for Assignment 2.
SYSTEM_NO_FACTS = SYSTEM.split("FACTS:", 1)[0] + "RULES:" + SYSTEM.split("RULES:", 1)[1]

QUESTIONS = [
    "How much does a dosa cost?",
    "Do you serve chicken biryani?",
    "What are your opening hours?",
    "What is the cost of 3 idlis?",
    "Do you deliver food to my hostel?",
    "Do you offer a 50% discount?",
    "How many orders can you serve at a time?",
    "Can I pre-order my food?",
    "Can I get shawarma at CampusBites?",
    "What is the combined cost of one dosa and one idli?",
]


def get_api_key():
    """Read the key safely; never hard-code it or display it."""
    key = os.getenv("GROQ_API_KEY")
    if not key:
        try:
            from google.colab import userdata
            key = userdata.get("GROQ_API_KEY")
        except Exception:
            raise SystemExit(
                "Set GROQ_API_KEY in your environment or enable the Colab secret."
            ) from None
    if not key:
        raise SystemExit("GROQ_API_KEY is empty.")
    return key


def create_client():
    from openai import OpenAI
    return OpenAI(api_key=get_api_key(), base_url=BASE_URL)


def ask(client, question, system=None, temperature=0.2):
    """Send one independent API request and return the response object."""
    messages = []
    if system is not None:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": question})
    return client.chat.completions.create(
        model=MODEL, temperature=temperature, messages=messages
    )


def first_call(client):
    print("First API call and system prompt experiments")
    general = "You are a friendly assistant."
    for question in [
        "Suggest a creative name for a college canteen.",
        "Explain artificial intelligence in simple words.",
        "Suggest five popular breakfast items for a college canteen.",
        "Write a catchy advertisement for a college canteen.",
    ]:
        response = ask(client, question, general)
        print(question, "\n", response.choices[0].message.content, "\n")

    question = "Suggest five breakfast items."
    specialized = (
        "You are a South Indian college canteen assistant. Suggest affordable "
        "vegetarian food suitable for Indian college students. Keep your answer short."
    )
    for prompt in [general, specialized]:
        response = ask(client, question, prompt)
        print(prompt, "\n", response.choices[0].message.content, "\n")


def temperature_experiment(client):
    """Assignment 1: three calls at each temperature, same question and prompt."""
    for temperature in [0.2, 1.2]:
        print("\nTemperature:", temperature)
        for i in range(3):
            response = ask(client, "Write one tagline for CampusBites.", SYSTEM, temperature)
            print("Attempt", i + 1)
            print(response.choices[0].message.content)


def hallucination_experiment(client):
    """Assignment 2: compare responses without and with business facts."""
    question = "Do you deliver food to Kakinada?"
    for label, prompt in [("Without facts", SYSTEM_NO_FACTS), ("With facts", SYSTEM)]:
        response = ask(client, question, prompt)
        print(label + ":", response.choices[0].message.content)


def memory_experiment(client):
    """Assignment 3: independent requests versus supplied conversation history."""
    introduction = "My name is Ravi."
    question = "What is my name?"
    first = ask(client, introduction)
    reply = first.choices[0].message.content
    print("Introduction:", reply)
    second = ask(client, question)
    print("Without history:", second.choices[0].message.content)

    # Reuse the actual first answer as the assistant message.
    messages = [
        {"role": "user", "content": introduction},
        {"role": "assistant", "content": reply or "Hello Ravi!"},
        {"role": "user", "content": question},
    ]
    third = client.chat.completions.create(
        model=MODEL, temperature=0.2, messages=messages
    )
    print("With history:", third.choices[0].message.content)


def token_experiment(client):
    """Assignment 4: compare provider-reported usage for English and Telugu."""
    for language, question in [
        ("English", "What is the price of a dosa?"),
        ("Telugu", "ఒక దోస ధర ఎంత?"),
    ]:
        response = ask(client, question)
        print("\n", language, sep="")
        print("Response:", response.choices[0].message.content)
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Completion tokens:", response.usage.completion_tokens)
        print("Total tokens:", response.usage.total_tokens)


def business_experiment(client):
    """Assignment 5: apply the business prompt to customer questions."""
    for question in QUESTIONS:
        response = ask(client, question, SYSTEM)
        print("Customer:", question)
        print("CampusBites:", response.choices[0].message.content, "\n")


def main():
    tasks = {
        "first": first_call,
        "temperature": temperature_experiment,
        "hallucination": hallucination_experiment,
        "memory": memory_experiment,
        "tokens": token_experiment,
        "business": business_experiment,
    }
    parser = argparse.ArgumentParser(description="CampusBites Day 1 practicals")
    parser.add_argument("task", nargs="?", default="business", choices=[*tasks, "all"],
                        help="Choose one experiment (default: business) or all")
    args = parser.parse_args()
    client = create_client()
    if args.task == "all":
        for name, experiment in tasks.items():
            print("\n=== " + name.upper() + " ===")
            experiment(client)
    else:
        tasks[args.task](client)


if __name__ == "__main__":
    main()
