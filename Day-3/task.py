"""Day 3: CampusBites LangChain assistant, evaluation and tool preparation."""

import argparse
import csv
import json
import os
from pathlib import Path

MODEL = "openai/gpt-oss-20b"
BUSINESS = "CampusBites"
TEST_PATH = Path(__file__).with_name("tests.csv")
MENU = {"idli": 20, "dosa": 35, "upma": 25, "poori": 40,
        "veg fried rice": 60, "tea": 10, "coffee": 15}
MAX_TURNS = 4

SYSTEM = """
ROLE:
You are the friendly customer support assistant
for CampusBites.

FACTS:
Idli costs Rs 20.
Dosa costs Rs 35.
Upma costs Rs 25.
Poori costs Rs 40.
Veg Fried Rice costs Rs 60.
Tea costs Rs 10.
Coffee costs Rs 15.

Opening hours: 8 AM to 5 PM.
Only vegetarian food is available.
Students can pre-order meals for campus pickup.
Bulk orders require two hours' notice.

RULES:
Never invent menu items, prices or offers.
Never promise delivery or exact pickup times.
If information is unavailable, ask the customer
to check with the canteen manager.
Calculate totals carefully.
Never claim an order has been placed or confirmed.

FORMAT:
Reply politely in under 50 words.
Use English or Telugu matching the customer.
"""

SYSTEM_V2 = SYSTEM.replace(
    "If information is unavailable, ask the customer\n"
    "to check with the canteen manager.",
    'If information is unavailable, explicitly say: '
    '"Please check with the canteen manager." '
    'Do not guess or make unsupported promises.'
)


def make_model(temperature: float = 0.3):
    """Create a Groq chat model using an environment variable or Colab Secret."""
    if not os.getenv("GROQ_API_KEY"):
        try:
            from google.colab import userdata
            key = userdata.get("GROQ_API_KEY")
            if key:
                os.environ["GROQ_API_KEY"] = key
        except Exception:
            raise RuntimeError("Set GROQ_API_KEY in your environment or Colab Secrets.") from None
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is missing.")
    from langchain_groq import ChatGroq
    return ChatGroq(model=MODEL, temperature=temperature)


def make_chain(llm, system: str = SYSTEM):
    """Compose a prompt, chat model and string parser using LCEL."""
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.output_parsers import StrOutputParser
    # SYSTEM has plain text menu facts, avoiding template brace conflicts.
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        MessagesPlaceholder("history"),
        ("human", "{question}")
    ])
    return prompt | llm | StrOutputParser()


def template_demo(llm):
    """Demonstrate a reusable business/question template."""
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the assistant for {business}. Answer in under 30 words."),
        ("human", "{question}")
    ])
    chain = prompt | llm | StrOutputParser()
    print(chain.invoke({"business": BUSINESS, "question": "Introduce yourself."}))


class CampusBitesChatbot:
    """Store successful conversation turns; send only recent complete pairs."""
    def __init__(self, chain):
        self.chain = chain
        self.history = []

    def ask(self, question: str) -> str:
        """Generate a response and store the successful conversation turn."""
        if not question.strip():
            raise ValueError("Enter a non-empty question.")
        answer = self.chain.invoke({
            "history": self.history[-2 * MAX_TURNS:],
            "question": question
        })
        if not isinstance(answer, str) or not answer.strip():
            raise RuntimeError("The model returned no text.")
        self.history.extend([("human", question), ("ai", answer)])
        return answer


def get_price(item: str, qty: int = 1) -> int:
    """Calculate the total price of a listed menu item in rupees."""
    item = item.lower().strip()
    if item not in MENU:
        raise ValueError("Item is not on the menu.")
    if type(qty) is not int or qty <= 0:
        raise ValueError("Quantity must be a positive integer.")
    return MENU[item] * qty


def check_availability(item: str) -> bool:
    """Check menu membership only; this does not verify real-time stock."""
    return item.lower().strip() in MENU


def read_tests(path=TEST_PATH):
    """Read and validate the workshop's two-column CSV test format."""
    with open(path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["question", "must_include"]:
            raise ValueError("CSV needs question,must_include columns.")
        rows = list(reader)
    if not rows or any(None in row or not (row.get("question") or "").strip()
                       or not (row.get("must_include") or "").strip() for row in rows):
        raise ValueError("CSV must contain non-empty questions and expected keywords.")
    return rows


def run_tests(test_chain, path=TEST_PATH):
    """Run independent keyword evaluations and preserve complete responses."""
    results = []
    for row in read_tests(path):
        question = row["question"]
        expected = row["must_include"]
        try:
            answer = test_chain.invoke({"history": [], "question": question})
            if not isinstance(answer, str) or not answer.strip():
                raise RuntimeError("Empty model response")
            ok = expected.lower() in answer.lower()
            status = "PASS" if ok else "FAIL"
        except Exception as exc:
            # Do not treat a transport or provider error as an incorrect answer.
            answer = f"Request failed: {type(exc).__name__}"
            ok = False
            status = "ERROR"
        results.append({"question": question, "must_include": expected,
                        "answer": answer, "passed": ok, "status": status})
        print(f"{status} | {question}\nExpected: {expected}\nAnswer: {answer}\n" + "-" * 60)
    passed = score(results)
    errors = sum(row["status"] == "ERROR" for row in results)
    print(f"{passed}/{len(results)} passed ({passed / len(results):.0%}); {errors} request error(s)")
    if errors:
        print("Incomplete evaluation: resolve request errors and rerun before comparing scores.")
    return results


def score(results) -> int:
    """Count keyword passes."""
    return sum(row["passed"] for row in results)


def run_experiments(path=TEST_PATH):
    """Compare the original and improved prompts, then run temperature 1.0 twice."""
    low = make_model(0.3)
    high = make_model(1.0)
    baseline = make_chain(low, SYSTEM)
    improved = make_chain(low, SYSTEM_V2)
    high_chain = make_chain(high, SYSTEM_V2)
    experiments = {}
    for label, chain in [("baseline_0.3", baseline), ("improved_0.3", improved),
                         ("high_1.0_run_1", high_chain), ("high_1.0_run_2", high_chain)]:
        print(f"\n=== {label} ===")
        experiments[label] = run_tests(chain, path)
    print("\n=== Comparison ===")
    for label, results in experiments.items():
        errors = sum(row["status"] == "ERROR" for row in results)
        print(f"{label}: {score(results)}/{len(results)} ({errors} errors)")
    if not any(r["status"] == "ERROR" for rows in experiments.values() for r in rows):
        base, better, first, second = experiments.values()
        change = 100 * (score(better) / len(better) - score(base) / len(base))
        different = sum(a["answer"] != b["answer"] for a, b in zip(first, second))
        print(f"Prompt pass-rate change: {change:+.1f} percentage points")
        print(f"High-temperature answers with different text: {different}/{len(first)}")
    return experiments


def agent_demo(llm):
    """Create the Day 3 agent shell; executable tools are introduced on Day 4."""
    from langchain.agents import create_agent
    agent = create_agent(model=llm, tools=[], system_prompt=SYSTEM)
    result = agent.invoke({"messages": [{"role": "user", "content": "How much does a dosa cost?"}]})
    print(result["messages"][-1].content)
    return result


def tool_demo():
    """Run the six local checks from the notebook."""
    assert get_price("dosa", 3) == 105
    assert get_price("idli", 5) == 100
    assert get_price("tea", 2) == 20
    assert get_price(" DOSA ", 2) == 70
    assert check_availability("dosa") is True
    assert check_availability("shawarma") is False
    print("All 6 function tests passed!")


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--mode", choices=["chat", "template", "tests", "experiments", "agent", "tools"], default="chat")
    cli.add_argument("--tests", type=Path, default=TEST_PATH)
    cli.add_argument("--results", type=Path, help="Optional JSON file to save live test results.")
    args = cli.parse_args()
    if args.mode == "tools":
        tool_demo()
        return
    if args.mode == "experiments":
        results = run_experiments(args.tests)
    else:
        llm = make_model()
        if args.mode == "template":
            template_demo(llm)
            return
        if args.mode == "agent":
            agent_demo(llm)
            return
        chain = make_chain(llm, SYSTEM if args.mode == "tests" else SYSTEM_V2)
        if args.mode == "tests":
            results = run_tests(chain, args.tests)
        else:
            bot = CampusBitesChatbot(chain)
            print("CampusBites | Type exit to quit.")
            while True:
                try:
                    question = input("You: ").strip()
                except (EOFError, KeyboardInterrupt):
                    break
                if question.lower() in {"exit", "quit", "bye"}:
                    break
                if not question:
                    continue
                try:
                    print("Bot:", bot.ask(question))
                except Exception as exc:
                    print(f"Bot: Request failed ({type(exc).__name__}). Please try again.")
            return
    if args.results:
        args.results.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved results: {args.results}")


if __name__ == "__main__":
    main()
