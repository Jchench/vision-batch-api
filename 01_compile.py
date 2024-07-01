import os
import re

def extract_page_number(filename):
    match = re.search(r'page_(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

def compile_texts(folder_path, output_file):
    try:
        # Ensure the folder path exists
        if not os.path.isdir(folder_path):
            print(f"Error: The folder path '{folder_path}' does not exist.")
            return

        # Get a sorted list of text files based on page number
        filenames = sorted(
            [f for f in os.listdir(folder_path) if f.endswith('.txt') and os.path.isfile(os.path.join(folder_path, f))],
            key=extract_page_number
        )

        if not filenames:
            print("No text files found in the specified folder.")
            return

        with open(output_file, 'w') as outfile:
            for filename in filenames:
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n')  # Add a newline character to separate files
                        print(f"Successfully added {filename}")
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        print(f"All text files have been compiled into {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

# Specify the folder containing the text files
folder_path = 'clean/PL110_289_results'

# Specify the name of the output file
output_file = 'clean/PL110_289_results/PL110_289.txt'

compile_texts(folder_path, output_file)
