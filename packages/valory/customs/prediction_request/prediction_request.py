# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023-2024 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
"""Contains the job definitions"""

from typing import Any, Dict, Optional, Tuple
import os
from openai import OpenAI
import json

client: Optional[OpenAI] = None


PREDICTION_PROMPT="""
You are an LLM inside a multi-agent system that takes in user questions about whether an event is likely to happen or not.
Answers to those questions should only be Y(for YES) or N (for NO).
You need to provide a YES/NO answer based on your training data.

Only respond with the format below using curly brackets to encapsulate the variables within a json dictionary object and no other text:

"response": "response"

USER_PROMPT:

{user_prompt}
"""


class OpenAIClientManager:
    """Client context manager for OpenAI."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def __enter__(self) -> OpenAI:
        global client
        if client is None:
            client = OpenAI(api_key=self.api_key)
        return client

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        global client
        if client is not None:
            client.close()
            client = None


DEFAULT_OPENAI_SETTINGS = {
    "max_tokens": 500,
    "temperature": 0.7,
}
PREFIX = "openai-"
ENGINES = {
    "chat": ["gpt-3.5-turbo", "gpt-4"],
    "completion": ["gpt-3.5-turbo-instruct"],
}
ALLOWED_TOOLS = [PREFIX + value for values in ENGINES.values() for value in values]


def run(**kwargs) -> Tuple[Optional[str], Optional[Dict[str, Any]], Any, Any]:
    """Run the task"""
    with OpenAIClientManager(kwargs["api_keys"]["openai"]):

        # Get the LLM params
        max_tokens = kwargs.get("max_tokens", DEFAULT_OPENAI_SETTINGS["max_tokens"])
        temperature = kwargs.get("temperature", DEFAULT_OPENAI_SETTINGS["temperature"])
        prompt = PREDICTION_PROMPT.replace("{user_prompt}", kwargs["prompt"])
        tool = kwargs["tool"]
        counter_callback = kwargs.get("counter_callback", None)

        # Check that the tool is available
        if tool not in ALLOWED_TOOLS:
            return (
                f"Tool {tool} is not in the list of supported tools.",
                None,
                None,
                None,
            )

        engine = tool.replace(PREFIX, "")

        # Call the LLM
        if engine in ENGINES["chat"]:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
            response = client.chat.completions.create(
                model=engine,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                n=1,
                timeout=120,
                stop=None,
            )
            return response.choices[0].message.content, prompt, None, None
        response = client.completions.create(
            model=engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            timeout=120,
            presence_penalty=0,
        )
        return response.choices[0].text, prompt, None, counter_callback


if __name__ == "__main__":
    openai_api_key = os.environ["OPENAI_API_KEY"]
    result = run(
        tool="openai-gpt-3.5-turbo",
        prompt="Will autonomous agents rule the world someday?",
        api_keys={"openai": openai_api_key}
    )
    print(f"Result: {result}")
    response = json.loads(result[0])
    print(response)