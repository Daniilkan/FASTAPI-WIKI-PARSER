import requests
import json

def get_summary(prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-r1",
        "messages": [
            {"role": "system", "content": "Ты — ассистент, делающий summary статьи."},
            {"role": "user", "content": "Сделай краткое summary без украшений и выделений текста, сохраняя важную информацию в самом начале: " + prompt}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
    )

    if response.status_code == 200:
        try:
            response_json = response.json()
            if "choices" in response_json:
                content = response_json["choices"][0]["message"].get("content", "")
                return content
            else:
                raise "Unexpected response format: 'choices' not found."
        except json.JSONDecodeError:
            raise "Error decoding JSON response."
    else:
        return f"Error: {response.status_code} - {response.text}"
