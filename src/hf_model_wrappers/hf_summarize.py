import os
import requests
from dotenv import load_dotenv

from transformers import AutoTokenizer

def bart_large_cnn(article_text):
    """summarizes input text bart_large_cnn model from HuggingFace"""

    # Load the BART tokenizer
    tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-cnn')

    # Tokenize the input text
    encoded_input = tokenizer(
        article_text,
        truncation=True,        # Ensure the input is truncated to fit the model
        max_length=512,         # Adjust based on your needs
        return_tensors='pt'     # We won't use this since the API expects plain text
    )

    # Decode the tokens back to text
    tokenized_text = tokenizer.decode(encoded_input['input_ids'][0], skip_special_tokens=True)

    # Send this tokenized text to the API
    payload = {
        "inputs": tokenized_text,
        "parameters": {"max_length": 100, "min_length": 30, "do_sample": False},
    }

    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    load_dotenv()
    HF_API_KEY = os.getenv('HUGGING_FACE_API_KEY')
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        summary_data = response.json()
        summary_text = summary_data[0]['summary_text']
        return summary_text
    else:
        print(f"Error during summarization: {response.text}")
        return
    