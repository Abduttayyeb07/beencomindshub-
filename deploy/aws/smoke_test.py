"""Exercise the model features Cowork relies on through the private gateway."""
from __future__ import annotations

import base64
import os

from openai import OpenAI


client = OpenAI(
    base_url=os.environ.get("MODEL_GATEWAY_URL", "http://127.0.0.1:4000/v1"),
    api_key=os.environ["LITELLM_MASTER_KEY"],
)
model = os.environ.get("COWORK_PLANNING_MODEL", "planning")

# 1. Basic response and usage accounting.
response = client.chat.completions.create(
    model=model, messages=[{"role": "user", "content": "Reply with OK"}], max_tokens=16
)
assert response.choices and response.usage

# 2. Streaming.
chunks = client.chat.completions.create(
    model=model, messages=[{"role": "user", "content": "Count from 1 to 3"}], stream=True
)
assert "".join(c.choices[0].delta.content or "" for c in chunks)

# 3. Forced tool call, used for tools and structured output.
tool = {"type": "function", "function": {
    "name": "echo", "description": "Echo text",
    "parameters": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]},
}}
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Call echo with text hello"}],
    tools=[tool], tool_choice={"type": "function", "function": {"name": "echo"}},
)
assert response.choices[0].message.tool_calls

# 4. Tiny PNG attachment / vision input.
png = base64.b64encode(
    base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
).decode()
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Describe this image briefly."},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{png}"}},
    ]}],
    max_tokens=40,
)
assert response.choices[0].message.content

print("PASS: response, usage, streaming, tools, and image attachment")

