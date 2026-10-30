import json
from anthropic import Anthropic

client = Anthropic()

# 1. What matters, and how much
WEIGHTS = {"accuracy":     0.4,
           "completeness": 0.3,
           "clarity":      0.2,
           "brevity":      0.1}

# 2. Tell the judge exactly how to reply
RESPONSE_FORMAT = """Reply with ONLY this JSON, scores 1-5:
{"accuracy": _, "completeness": _,
 "clarity": _, "brevity": _}"""

# 3. The judge
def judge(query, user_response):
    prompt = f"""Score the RESPONSE 1-5 on:
accuracy, completeness, clarity, brevity.

QUERY: {query}
RESPONSE: {user_response}

{RESPONSE_FORMAT}"""
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user",
                   "content": prompt}],
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
