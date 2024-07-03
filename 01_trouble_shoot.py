import json
import base64
import requests
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Verify the image format and size
def verify_image(image_path):
    valid_formats = ['jpeg', 'png', 'gif', 'webp']
    file_size = os.path.getsize(image_path)
    file_extension = image_path.split('.')[-1].lower()

    if file_extension not in valid_formats:
        raise ValueError(f"Unsupported image format: {file_extension}")
    if file_size > 20 * 1024 * 1024:
        raise ValueError(f"File size exceeds 20 MB: {file_size / (1024 * 1024)} MB")
    return True

# List of specific page files to process
pages_to_process = ['page_1.jpeg'
]

# Folder containing the images
image_folder = "pdf_pages/PL101_073"
base_folder_name = os.path.basename(image_folder)
results_folder = os.path.join("clean", f"{base_folder_name}_results")

# Create the results folder if it doesn't exist
os.makedirs(results_folder, exist_ok=True)

# Get list of image paths from the folder, filtering only those in the pages_to_process list
image_paths = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.lower() in pages_to_process]

# OpenAI API Key
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()

if not api_key:
    raise ValueError("API key not found. Set the OPENAI_API_KEY environment variable.")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Process each image in the folder
for image_path in image_paths:
    retry_count = 0
    max_retries = 3
    while retry_count < max_retries:
        try:
            verify_image(image_path)
            encoded_image = encode_image(image_path)

            # Construct the payload for the single image
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Transcribe this image. Do not include any other text besides the transcription."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ]

            payload = {
                "model": "gpt-4o",
                "messages": messages
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            # Check if the response is successful
            if response.status_code == 200:
                # Parse the response as JSON
                response_data = response.json()
                
                # Extract the content from the response
                content = response_data['choices'][0]['message']['content']

                # Use the original image file name for the text file
                file_name = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
                file_path = os.path.join(results_folder, file_name)

                # Save the content to a text file
                with open(file_path, 'w') as file:
                    file.write(content)

                logging.info(f"Content saved to {file_path}")
                break  # Exit the retry loop if successful
            else:
                # Print an error message if the request failed
                logging.error(f"Failed to retrieve data for {image_path}: {response.status_code}, {response.text}")
                retry_count += 1
                time.sleep(2 ** retry_count)  # Exponential backoff before retrying
                if retry_count == max_retries:
                    logging.error(f"Max retries reached for {image_path}. Moving to next image.")

        except ValueError as e:
            logging.error(f"Error with image {image_path}: {e}")
            break  # Exit the loop if there's an error with the image
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error for {image_path}: {e}")
            retry_count += 1
            time.sleep(2 ** retry_count)  # Exponential backoff before retrying
