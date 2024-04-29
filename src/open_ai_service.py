import json
import re
import requests
from .prompts import items_prompt, header_prompt, focus_prompt
from .references.navalmed import get_data
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


async def handle_image(images: list):
    header = await query(header_prompt, images[0])
    json = header['data']
    input = header['usage']['prompt_tokens']
    output = header['usage']['completion_tokens']
    line_number = 1
    items = []

    for image in images:
        result = await query(items_prompt, image, True)
        input += result['usage']['prompt_tokens']
        output += result['usage']['completion_tokens']

        for item in result['data']['items']:
            item['line_number'] = line_number
            item['impa'] = extract_number(item['impa'])
            items.append(item)

            line_number += 1

    json['cost'] = get_cost(input, output)
    json['items'] = items

    return json


def get_cost(input_tokens, output_tokens):
    input_cost_per_token = 10 / 1000000
    output_cost_per_token = 30 / 10000000

    return (input_tokens * input_cost_per_token) + (output_tokens * output_cost_per_token)


def extract_number(text):
    if text is None:
        return None

    match = re.search(r'\d+', text)

    if match:
        return match.group()

    return None


async def query(prompt, image, isItems=False):
    content = []

    if isItems is True:
        content.append(
            {"type": "text", "text": focus_prompt})

        content.append({"type": "image_url", "image_url": {
            "url": f"{get_data()}"}}
        )

    content.append(
        {"type": "text", "text": prompt})

    content.append(
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image}",
                "detail": "high"
            }
        }
    )

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    response_data = response.json()

    usage = {}
    usage['prompt_tokens'] = 0
    usage['completion_tokens'] = 0
    result = {}

    if 'usage' in response_data:
        usage['prompt_tokens'] = response_data["usage"]["prompt_tokens"]
        usage['completion_tokens'] = response_data["usage"]["completion_tokens"]

    if 'choices' in response_data and response_data['choices']:
        first_choice = response_data['choices'][0]

        if 'message' in first_choice and 'content' in first_choice['message']:
            data = json.loads(first_choice['message']['content'])
            result['data'] = data
            result['usage'] = usage
            return result

    return "No content found in the response"
