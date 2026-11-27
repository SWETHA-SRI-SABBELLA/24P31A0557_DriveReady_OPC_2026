# Day 2 — Prompts, Memory and Python for Agents

**Drive Ready OPC 2026 | CampusBites AI Assistant | Roll No. 24P31A0557**

## Objective

Build a context-aware customer support chatbot for a fictional vegetarian campus canteen using Groq, Python and prompt engineering. This day prepares Python functions for later agent tool integration.

## Files

- `task.py` — standalone implementation of all five official assignments and local Python demonstrations.
- `Prompts_Memory_Python.ipynb` — Colab notebook containing the step-by-step exercises (upload separately from Colab).
- `README.md` — project documentation.

## Concepts covered

1. System, user and assistant message roles
2. System prompt engineering: Role, Facts, Rules, Format
3. Few-shot prompting
4. JSON structured output and `json.loads()`
5. Conversation history and memory trimming
6. Python dictionaries, `.get()`, `json.dumps()` and input normalization
7. Functions, type hints, docstrings and validation
8. Decorators, `functools.wraps`, `*args` and `**kwargs`
9. Exception handling for API, JSON and input failures

## Business catalogue

| Item | Price (INR) |
| --- | ---: |
| Idli | 20 |
| Dosa | 35 |
| Upma | 25 |
| Poori | 40 |
| Veg fried rice | 60 |
| Tea | 10 |
| Coffee | 15 |

Business facts: opening hours are 8 AM to 5 PM; vegetarian food only; pre-orders for campus pickup; bulk orders require two hours' notice. Delivery service, live stock, kitchen capacity and discounts are not established facts.

## Official assignments

| No. | Exercise | Implementation |
| --- | --- | --- |
| 1 | Remove and restore rules; ask whether delivery in one hour is possible | `prompt_experiment()` |
| 2 | Three few-shot examples; classify five unseen customer messages | `classifier_experiment()` |
| 3 | Extract name, item, qty, date and eggless; parse JSON in try/except | `json_experiment()` / `extract_order()` |
| 4 | Set MAX_TURNS to 2; introduce a name, chat for three turns, then ask the name | `memory_experiment()` |
| 5 | Rebuild the trainer's chatbot for CampusBites with a menu dictionary, documented functions, system prompt, logging, memory and exceptions | `CampusBitesChatbot`, `interactive_chat()` |

### Expected observations

- Rules help restrict unsupported promises; they do not guarantee model compliance. The first experiment changes only the rules while holding other prompt parts and temperature constant.
- Three labelled examples demonstrate the required categories. Expected labels for the five tests are `order`, `question`, `complaint`, `order`, `question`.
- JSON text becomes a Python dictionary using `json.loads()`. Missing values become `None`. Parsing and basic field validation do not prove semantic accuracy or confirm an order.
- The trainer's `MAX_TURNS` in Assignment 4 counts individual non-system messages. A limit of 2 may exclude the customer's earlier name; the full Python history still exists. The program prints the actual final API request for inspection.
- The final chatbot keeps up to four previous complete question/reply pairs, plus the system message and current request. It records only successful, nonempty responses. It catches rate limit, authentication and connection errors. Its menu functions are not yet connected as LLM tools.
- The exact live experimental responses and final chatbot checklist results are not recorded here because they have not been supplied for independent verification. Preserve the actual outputs in the submitted notebook.

## Implementation improvements

This source adapts the trainer's Sweet Crumbs example to CampusBites. It preserves the original message-slicing experiment for Assignment 4, but uses complete turn pairs in the final chatbot. It adds quantity and item validation, JSON shape/type checks, nulls for missing values, and rules against claiming real order placement or guaranteed delivery/pickup times. The source is organized as a standalone CLI; the notebook uses separate teaching cells.

## Setup and execution

Install the OpenAI Python SDK:

```bash
python -m pip install openai
```

Set `GROQ_API_KEY` in your local environment or in Colab Secrets (enable notebook access). Do not include the actual key in source code, notebook outputs or commits.

In Windows PowerShell, if the variable is not already set, use a local environment variable with your own key. Do not commit the command with the real key or share a screenshot of it.

```powershell
$env:GROQ_API_KEY = "<your-key>"
```

The model used in the workshop is `openai/gpt-oss-20b`, accessed through the Groq OpenAI-compatible endpoint.

Run from the Day-2 folder:

```bash
python task.py --help
python task.py --experiment python
python task.py --experiment prompts
python task.py --experiment classifier
python task.py --experiment json
python task.py --experiment memory
python task.py --experiment chat
```

`python` runs local demonstrations without a key or SDK. The other modes require the SDK, internet access and a working Groq key. `--experiment all` runs the demonstrations and all experiments before starting the interactive chat. Type `exit` to stop the chat.

## Test evidence

Assessment score: **17/18 (94.44%)**. The missed question was Q12: JSON booleans use lowercase `true`/`false`, not Python `True`/`False`.

Source validation performed during preparation:

- Python syntax compilation: passed.
- CLI help and local Python demonstration: passed.
- Local pricing, menu lookup, validation, decorator metadata, request construction, JSON parsing and validation, memory slicing, failure handling and recovery: **27/27 assertions passed** using local logic and mocked API responses/exception classes.

The OpenAI SDK was not available in the source-preparation environment, so API-related checks used a simulated client and exception classes. No live Groq request was made during source preparation. These checks are not evidence of live model accuracy; run the experiments in Colab and retain actual outputs.

Example live chatbot test plan: introduce Ravi; request three dosas for tomorrow; add two teas; ask the name and total (expected Rs 125); ask for delivery in ten minutes (no guaranteed delivery); type `exit`. No real order should be created. The expected bill is for evaluation only: conversational calculations still come from the LLM rather than autonomous calls to the Python pricing function.

## Day 3 preparation

The catalogue is defined as `MENU` in `task.py`. Ten customer questions are included as `QUESTIONS`:

1. How much does a dosa cost?
2. Do you serve chicken biryani?
3. What are your opening hours?
4. What is the cost of 3 idlis?
5. Do you deliver food to my hostel?
6. Do you offer a 50% discount?
7. How many orders can you serve at a time?
8. Can I pre-order my food?
9. Do you serve shawarma?
10. What is the combined cost of one dosa and one idli?

## Limitations

CampusBites is a learning prototype, not a production ordering application. It has no database, real-time stock data, persistent memory, payment, actual order placement or autonomous tool execution. Context trimming can omit important customer details; system prompts do not guarantee correct responses. Specific API errors are handled in the chatbot, not every possible exception. Separate experimental functions can still raise API errors. Future workshop lessons will introduce LangChain and agent tools.
