import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Function to extract keywords from a list of titles
def extract_keywords(title):
    # Your Hugging Face API key
    API_KEY = os.getenv('HUGGING_FACE_API_KEY')

    # The model we are going to use
    MODEL_NAME = "ilsilfverskiold/tech-keywords-extractor"
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    def query(payload, retries=5, delay=60):
        for attempt in range(retries):
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                try:
                    error_info = response.json()
                    print(f"Model is loading, retrying in {delay} seconds... Estimated time: {error_info.get('estimated_time', 'unknown')}")
                    time.sleep(delay)
                except ValueError:  # In case the response is not JSON or doesn't have the expected fields
                    print(f"Model is loading, retrying in {delay} seconds...")
                    time.sleep(delay)
            else:
                raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
        raise Exception("Max retries exceeded")

    payload = {"inputs": title}
    results = query(payload)
    extracted_keywords = []
    extracted_keywords = results[0]['generated_text'].split(", ")
    no_spaces_extracted_keywords = [element.replace(" ", "") for element in extracted_keywords]

    return no_spaces_extracted_keywords

def main(title):
    extracted_keywords = extract_keywords(title)
    print(extracted_keywords)

if __name__ == "__main__": 
    main("Miley Cyrus’s New Music Video Is Filled with Vintage Fashion Treasures.")