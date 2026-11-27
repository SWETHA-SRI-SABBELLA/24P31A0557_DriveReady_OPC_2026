# Day 1 — LLM Fundamentals and First API Call

**Program:** Drive Ready – AI Agents | OPC 2026  
**Case study:** CampusBites – AI Campus Canteen Assistant

## Objective

Learn how a pre-trained large language model (LLM) can be accessed through an API, guided with business-specific prompts, and evaluated through simple experiments. CampusBites is a fictional vegetarian college canteen used for practice, not an operational service.

## Topics covered

- AI applications, LLMs and next-token prediction
- Groq API, API clients and secure API key management
- System, user and assistant messages; Role, Facts, Rules and Format
- Tokens, temperature, context windows and hallucination
- Stateless API requests and explicit conversation history
- Responsibilities of an AI application engineer

## Files

| File | Purpose |
| --- | --- |
| `task.py` | Consolidated Python source for the first API call and all five Day 1 assignments |
| `LLM_Fundamentals.ipynb` | Original Google Colab practical work and outputs (uploaded separately) |
| `README.md` | Task description, implementation, observations and next-day preparation |

## Implementation

Python uses the OpenAI-compatible SDK to send requests to Groq (`https://api.groq.com/openai/v1`) with the `openai/gpt-oss-20b` model. A system prompt defines CampusBites' menu, prices, hours and rules. The model generates an answer to each customer message. The program also exposes separate experiments for temperature, hallucination, history and token usage.

### Business facts

| Menu item | Price (INR) |
| --- | ---: |
| Idli | 20 |
| Dosa | 35 |
| Upma | 25 |
| Poori | 40 |
| Veg Fried Rice | 60 |
| Tea | 10 |
| Coffee | 15 |

Opening hours: 8 AM–5 PM; vegetarian food only; pre-orders for campus pickup; bulk orders require two hours' notice. These are sample policies. The prompt prohibits invented menu items, prices and offers, prohibits exact pickup-time promises, and directs the assistant to acknowledge missing information.

## Day 1 practical assignments and observations

### 1. Temperature

The same tagline request was run three times at each temperature.

| Attempt | Temperature 0.2 | Temperature 1.2 |
| --- | --- | --- |
| 1 | CampusBites: Fresh Vegetarian Feasts, Anytime, Anywhere. | CampusBites: Fresh, veggie-only meals that fuel your campus hustle. |
| 2 | CampusBites: Fresh, Flavorful, and Always on Time for Your Campus Life. | Fuel Your Studies, One Bite at a Time. |
| 3 | CampusBites: Fresh Vegetarian Flavors, Anytime on Campus. | CampusBites: Fresh Veg Bites, Campus-Ready! |

The higher-temperature examples showed greater variety in this run. Low temperature did not guarantee accuracy: “Anytime, Anywhere” and “Always on Time” are inconsistent with or unsupported by the sample policies.

### 2. Hallucination

Asked the same delivery question with and without the FACTS section, keeping the remaining prompt and temperature unchanged. The experiment was reported completed; the exact responses were not supplied for this README. The comparison is intended to show how grounding answers in facts can reduce unsupported claims. Rules alone may also lead a model to admit uncertainty.

### 3. No memory

Compared two separate API calls (introducing a name, then asking for it) with a request containing the previous conversation. The experiment was reported completed; the exact outputs were not supplied for this README. Expected behaviour: independent calls do not automatically carry conversation history, while supplied history lets the model use the name.

### 4. English vs Telugu token usage

Latest reported experiment results:

| Metric | English | Telugu |
| --- | ---: | ---: |
| Prompt tokens | 79 | 80 |
| Completion tokens | 98 | 151 |
| Total tokens | 177 | 231 |

Telugu used one additional prompt token and 53 additional completion tokens in this run. Token usage depends on the model tokenizer, text, and generated response. One experiment does not establish a universal language comparison.

### 5. Own business system prompt

Created a system prompt with five facts, three rules, a role and a response format. Six manually checked responses satisfied the basic expected checks:

| Question | Reported response summary |
| --- | --- |
| Dosa price | Rs 35 |
| Chicken biryani | Vegetarian items only; not on menu |
| Opening hours | 8 AM–5 PM |
| Three idlis | Rs 60 |
| Hostel delivery | No delivery; campus pickup |
| 50% discount | Unknown; referred to canteen manager |

Two limitations were noticed: the opening-hours answer said “daily” without a specified operating-days policy, and the discount answer promised follow-up even though no manager-contact tool exists. Basic checks are not proof of complete correctness. The original practice prompt is retained in `task.py` for reproducibility; these limitations are candidates for later improvements.

## Preparation for Day 2 — Ten customer questions

1. How much does a dosa cost?
2. Do you serve chicken biryani?
3. What are your opening hours?
4. What is the cost of 3 idlis?
5. Do you deliver food to my hostel?
6. Do you offer a 50% discount?
7. How many orders can you serve at a time?
8. Can I pre-order my food?
9. Can I get shawarma at CampusBites?
10. What is the combined cost of one dosa and one idli?

The last four questions are prepared for subsequent testing; their actual outputs were not supplied. The expected combined price is Rs 55. Order capacity is unspecified and should not be invented.

## How to run

Install the dependency:

```bash
pip install openai
```

Set `GROQ_API_KEY` securely in your environment (or create a Colab secret with that name and enable notebook access). Never commit or print the key.

Run a single experiment:

```bash
python task.py business
python task.py temperature
python task.py hallucination
python task.py memory
python task.py tokens
python task.py first
```

Run all experiments with `python task.py all`. Each experiment makes live API calls and consumes quota; results may vary. In Colab, upload the file and use `!python task.py business` with the secret enabled, or run the original notebook cells directly.

## Learning assessment and status

- Day 1 HTML assignments: 5/5 reported completed.
- Ten customer questions: prepared.
- Day 1 MCQ assessment: 16/18.
- Additional trainer notebook demonstrations (ChatGroq and Prompt Guard): not yet confirmed as performed.
- Current implementation: prompt-based assistant, not yet a tool-enabled AI agent.

The consolidated script was checked locally for syntax and basic request construction; live API results above are the student's reported Colab observations, not a fresh execution of this file.
