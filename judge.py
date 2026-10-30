import json
from anthropic import Anthropic

client = Anthropic()

# 1. What matters, and how much
WEIGHTS = {"correctness": 0.4,
           "coverage":    0.3,
           "coherence":   0.2,
           "conciseness": 0.1}

# 2. Force scores 1-5, as JSON
SCORE = {"type": "integer",
         "enum": [1, 2, 3, 4, 5]}
SCHEMA = {
  "type": "object",
  "properties": {k: SCORE for k in WEIGHTS},
  "required": list(WEIGHTS),
  "additionalProperties": False,
}

# 3. The judge
def judge(question, answer):
    prompt = f"""Score the ANSWER 1-5 on:
correctness, coverage, coherence, conciseness.

QUESTION: {question}
ANSWER: {answer}"""
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user",
                   "content": prompt}],
        output_config={"format": {
            "type": "json_schema",
            "schema": SCHEMA}},
    )
    return json.loads(resp.content[0].text)

# 4. One weighted number
def weighted(scores):
    return sum(scores[k] * w
               for k, w in WEIGHTS.items())

scores = judge(
    "How do I reset my password?",
    "Open Settings, tap Reset password, "
    "and check your inbox.")
print(scores, round(weighted(scores), 1))
