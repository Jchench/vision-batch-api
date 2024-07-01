import json
import base64
import requests
import os

# Read API key from file
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()

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

# Function to process images in a folder
def get_image_paths(folder_path):
    image_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.webp')):
                image_paths.append(os.path.join(root, file))
    return image_paths

def process_images_in_folder(folder_path):
    image_paths = get_image_paths(folder_path)
    encoded_images = []
    failures = []
    for image_path in image_paths:
        try:
            verify_image(image_path)
            encoded_images.append((image_path, encode_image(image_path)))
        except ValueError as e:
            print(f"Error with image {image_path}: {e}")
            failures.append(image_path)
    return encoded_images, failures

def upload_image(encoded_image, headers):
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Transcribe these images. Do not include any other text besides the transcription."
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
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response

def process_images_by_batches(encoded_images, headers):
    batch_record = {}
    failures = []

    for idx, (image_path, encoded_image) in enumerate(encoded_images):
        response = upload_image(encoded_image, headers)
        
        if response.status_code == 200:
            batch_record[image_path] = f"Batch {idx + 1}"
        else:
            print(f"Failed to process image {image_path}: {response.status_code}, {response.text}")
            failures.append(image_path)

    return batch_record, failures

def resubmit_failed_images(failures, headers):
    for image_path in failures:
        encoded_image = encode_image(image_path)
        response = upload_image(encoded_image, headers)
        if response.status_code == 200:
            print(f"Successfully resubmitted image {image_path}")
        else:
            print(f"Failed to resubmit image {image_path}: {response.status_code}, {response.text}")

# Usage example
folder_path = "PL110_289_test"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

encoded_images, initial_failures = process_images_in_folder(folder_path)
batch_record, failures = process_images_by_batches(encoded_images, headers)

# Log batch record to reconstruct later
print("Batch Record:", batch_record)

# Handle resubmission of failed images
if failures:
    print("Resubmitting failed images...")
    resubmit_failed_images(failures, headers)

# Save the batch record
batch_record_path = os.path.join('clean', 'PL110_289_results', 'batch_record.json')
os.makedirs(os.path.dirname(batch_record_path), exist_ok=True)
with open(batch_record_path, 'w') as file:
    json.dump(batch_record, file)

print(f"Batch record saved to {batch_record_path}")
