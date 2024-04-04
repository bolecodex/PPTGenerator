import requests

def generate_image(prompt):
    api_key = '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'  # Replace with your OpenAI API key
    endpoint = 'https://api.openai.com/v1/images/generations'  # Endpoint for image generation

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text

# Example usage
prompt = "Volkswagen CompanyLogo"
result = generate_image(prompt)
print(result)
