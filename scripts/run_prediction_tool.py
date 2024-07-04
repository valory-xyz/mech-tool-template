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
"""Script to call a tool"""

from dotenv import load_dotenv
from packages.valory.customs.prediction_request.prediction_request import run
import json
import os

MODELS = [
    "meta-llama/llama-3-8b-instruct:free",
    "google/gemma-2-9b-it:free",
    "nousresearch/nous-capybara-7b:free",
]

if __name__ == "__main__":

    # Load the API key
    load_dotenv()
    openrouter_api_key = os.environ["OPENROUTER_API_KEY"]

    # Call the tool
    result = run(
        prompt="Will autonomous agents play an important role on the economy someday?",
        api_keys={"openrouter": openrouter_api_key},
        model=MODELS[2]
    )

    # Print the result
    print(f"Result: {result}")
    try:
        print(json.loads(result[0]))  # type: ignore
    except json.decoder.JSONDecodeError:
        pass