import json
import os

# Function to read the batch record
def fetch_batch_record(file_path):
    if not os.path.exists(file_path):
        print(f"Batch record file {file_path} does not exist.")
        return None
    with open(file_path, 'r') as file:
        batch_record = json.load(file)
    return batch_record

# Usage example
batch_record_path = os.path.join('clean', 'PL110_289_results', 'batch_record.json')
batch_record = fetch_batch_record(batch_record_path)

if batch_record is not None:
    print("Batch Record:", batch_record)
else:
    print("No batch record found.")
