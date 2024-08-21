import os
import requests
import io
from dotenv import load_dotenv
from PIL import Image
import base64

# Load environment variables
load_dotenv()

# Hugging Face API Key from environment variables
HF_API_KEY = os.getenv('HUGGING_FACE_API_KEY')
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def query(api_url, payload):
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def encode_image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

def sd_xl_base_with_refiner(text):
    # Step A: create first image (without refinement)
    # create payload
    payload_1 = {"inputs": text,
                "parameters": {
                    "width": 1024,
                    "height": 1024,
                    "steps": 200,
                    "seed": 50,
                    "cfg_scale": 15
                }
            }

    initial_image_bytes = query(
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0", 
            payload_1
        )

    if initial_image_bytes:
        initial_image = Image.open(io.BytesIO(initial_image_bytes))
        # Convert the PIL Image to bytes for base64 encoding
        buf = io.BytesIO()
        initial_image.save(buf, format='PNG')
        initial_image.save('io_files/non_refined_image.png')
        image_bytes_for_refinement = buf.getvalue()
        encoded_image = encode_image_to_base64(image_bytes_for_refinement)
    else:
        print("Failed to generate the initial image.")
        exit()

    # Step B: Refine the Image using base64 encoded image
    payload_2 = {"inputs": encoded_image,
                 "parameters": {"strength": 0.1, "num_inference_steps": 100}
                }
    refined_image_bytes = query(
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-refiner-1.0",
            payload_2
    )

    if refined_image_bytes:
        refined_image = Image.open(io.BytesIO(refined_image_bytes))
        refined_image.save('io_files/refined_output_image.png')
        print("Refined image successfully saved as refined_output_image.png")
    else:
        print("Failed to refine the image.")

if __name__ == "__main__":
    title="Why Are We So Obsessed With What Celebrities Wear to Court?"
    text = """Visualize the essence of the following headline in an image that \
              captures the mood and significance of the title \
              {title}. The image should convey the atmosphere of a rich, classy \
              and prestigious fashion news outlet or magazine. \
              The image should not be low-quality. The image should not be anime. \
              The image should not be a cartoon. The image should not look unprofessional. \
              The image should not include ugly people. The image should not include \
              deformed people. There should be no missing limbs. \
              There should be no missing fingers.""".format(title=title)

    sd_xl_base_with_refiner(text)
