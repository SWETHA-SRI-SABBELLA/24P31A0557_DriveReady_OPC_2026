# Day 3 — Your First Agent and LangChain

**Project:** CampusBites — Campus Canteen Assistant  
**Program:** Drive Ready OPC 2026  
**Roll number:** 24P31A0557  
**Assessment:** 16/16 (all eight topic quizzes, as reported by the student)

## Objective

Rebuild the Day 2 chatbot using LangChain, understand the difference between a chatbot and an agent, evaluate responses systematically, and prepare two Python functions for Day 4 tool integration. CampusBites is a workshop case study, not a live ordering system.

## Concepts covered

| Topic | Learning outcome |
| --- | --- |
| 1. Chatbot vs agent | A chatbot responds; an agent can select actions and use tools to achieve a goal. |
| 2. Four parts of an agent | Brain (LLM), instructions (system prompt), tools (functions), and memory (conversation history). |
| 3. Agent loop (ReAct) | Think, act, observe, repeat; stop at a final answer or safety limit. The application executes tools. |
| 4. Three levels | Traditional software follows rules, generative AI produces content, agentic AI selects actions. |
| 5. Agent or not? | Choose the simplest adequate approach. |
| 6. Why LangChain? | Shared model interface and reusable components. |
| 7. LangChain basics | ChatGroq, ChatPromptTemplate, MessagesPlaceholder, LCEL, StrOutputParser. |
| 8. Testing | CSV-based keyword evaluation, pass rates, prompt improvement and regression testing. |

## Business facts

| Menu item | Price (INR) |
| --- | ---: |
| Idli | 20 |
| Dosa | 35 |
| Upma | 25 |
| Poori | 40 |
| Veg Fried Rice | 60 |
| Tea | 10 |
| Coffee | 15 |

Opening hours: 8 AM–5 PM. Vegetarian food only. Pre-orders are for campus pickup. Bulk orders require two hours' notice. Unknown information must be referred to the canteen manager. The assistant must not invent discounts, delivery or pickup promises, or claim to have placed an order.

## Architecture

```text
Question + recent conversation history
            |
            v
ChatPromptTemplate + MessagesPlaceholder
            |
            v
ChatGroq (openai/gpt-oss-20b)
            |
            v
StrOutputParser -> answer string
            |
            v
Store successful conversation turn
```

LCEL composition: `chain = prompt | llm | StrOutputParser()`.

The notebook demonstrates manual history insertion. The standalone script sends the four most recent completed turns plus the current question, and retains successful turns in memory. No persistent user memory is implemented.

## Official assignments (student's 30%)

### 1. Customise the business prompt

`SYSTEM` contains CampusBites' role, menu, facts, rules and response format. The reusable template demo fills the `business` variable with `CampusBites` and accepts a dynamic `question`. Menu facts are plain text to avoid accidental template placeholders in JSON braces.

### 2. Prepare and execute ten customer tests

`tests.csv` contains the ten previously prepared customer questions and expected keywords. `run_tests()` evaluates every question using an empty history, prints the full response and status, and returns structured results. Pass rate = keyword passes / total test cases × 100. Transport/model errors are marked `ERROR`, not ordinary incorrect answers; an error-containing run is incomplete and should be repeated before comparison.

### 3. Improve the prompt and rerun the tests

`SYSTEM_V2` replaces the original unknown-information rule with a more explicit instruction: “Please check with the canteen manager.” It also tells the model not to guess or make unsupported promises. Compare both prompts at temperature 0.3 using the same CSV. Rerunning all tests after a change is regression testing.

### 4. Test temperature 1.0 twice

Keep the improved prompt and model identifier unchanged, set temperature to 1.0, and run the same ten tests twice. Compare keyword pass rates and the actual answer text. A higher temperature may change the response without changing the score.

#### Live experiment results

Fill these rows with actual Colab or terminal results; no live scores have been supplied for this submission draft.

### Live Experiment Results

| Run | Prompt | Temperature | Passed / 10 | Pass Rate |
|---|---|---:|---:|---:|
| Baseline | Original | 0.3 | 9/10 | 90% |
| Improved | V2 | 0.3 | 7/10 | 70% |
| High Temperature Run 1 | V2 | 1.0 | 8/10 | 80% |
| High Temperature Run 2 | V2 | 1.0 | 8/10 | 80% |

### Observations

- The modified prompt decreased the keyword pass rate by 20 percentage points.
- Both high-temperature experiments achieved an 80% pass rate, although their generated responses differed.
- Some correct answers failed because of Unicode whitespace and alternative wording.
- Keyword matching alone cannot guarantee factual correctness.
- Some responses introduced unsupported ordering and delivery information.
- Regression testing is important after every prompt modification.

### Verification

- Day 3 assessment: 16/16.
- Python pricing and menu availability tests: 6/6 passed.
- LangChain agent demonstration: successful response recorded.
- All four experiment outputs are available in the submitted Colab notebook.

- Prompt improvement in percentage points: pending actual results.
- Differences between the two high-temperature runs: pending actual results.
- Limitation: keyword matching is a basic workshop evaluation, not proof of semantic correctness. For example, a wrong answer may still contain the expected word, and a correct answer may use an alternative phrase. Review actual responses for accuracy, unsupported promises and rule adherence.

### 5. Agent or not?

| CampusBites job | Approach | Reason |
| --- | --- | --- |
| Calculate a bill | Plain code | Known formula and exact menu prices. |
| Write a promotional advertisement | One LLM call | Generate a single piece of text. |
| Resolve a complex customer order | Agent | Potentially dynamic selection of lookup and authorised order tools, based on returned information. |

The agent-based order workflow is a proposed future feature, not an implemented order system.

## First agent demonstration

`create_agent(model=llm, tools=[], system_prompt=SYSTEM)` creates the agent shell. It can respond using its model and instructions but cannot execute local business tools. Real tool integration is reserved for Day 4, as required by the workshop.

## Preparation for Day 4

- `get_price(item: str, qty: int = 1) -> int`: normalises the item name, validates membership and positive integer quantity, then calculates the total price.
- `check_availability(item: str) -> bool`: checks whether the item is listed on the menu. It does not check live kitchen inventory.

Both functions have type hints and docstrings. They remain ordinary Python functions for Day 3.

## How to run

Install compatible packages together:

```bash
python -m pip install -U langchain langchain-core langchain-groq
```

Set your own `GROQ_API_KEY` as an environment variable. In Colab, enable notebook access to the existing `GROQ_API_KEY` secret. Never include the key in source files, output or GitHub commits. Restart the Colab session after upgrading already-imported packages, then rerun setup cells in order.

From the Day-3 directory:

```bash
python task.py --mode tools
python task.py --mode template
python task.py --mode chat
python task.py --mode tests
python task.py --mode experiments --results experiment_results.json
python task.py --mode agent
```

`--mode tools` runs locally without any API key. The experiments issue forty logical model invocations (four runs of ten cases); provider retries may make extra requests. The optional JSON file preserves answers and statuses for review. Do not publish sensitive conversation content.

## Verification and limitations

- Python syntax compilation: passed.
- CLI help and six standalone tool assertions: passed.
- Local and mocked assertions: 33/33 passed, covering pricing, input validation, CSV structure, independent test context, pass/fail/error handling, history trimming and experiment configuration.
- These checks did not call Groq or exercise installed LangChain integrations. The execution environment used for the local checks did not have LangChain installed. Live API runs and the empty-tool agent demonstration must be verified in Colab or a configured local environment.
- The student's own notebook and live outputs have not been independently inspected for this submission. Keep the genuine notebook and record actual scores before marking the experiments complete.

## Submission files

```text
Day-3/
├── First_AI_Agent_LangChain.ipynb  # student's own Colab notebook
├── task.py
├── tests.csv
└── README.md
```

Reference: Drive Ready Day 3 tutorial, *Your first agent: what an agent is, and LangChain*, and the trainer's Day 1–3 notebook. Bakery examples adapted to CampusBites.
