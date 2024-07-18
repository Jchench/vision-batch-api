from pdf2image import convert_from_path
import os

# Path to the directory containing PDFs
pdf_folder_path = 'pdf_3'

# Path to the directory where images will be saved
output_base_folder = 'pdf_pages'

# Create the base output directory if it doesn't exist
if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

# Iterate through all files in the specified folder
for filename in os.listdir(pdf_folder_path):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder_path, filename)
        
        # Path to the directory where images for this PDF will be saved
        output_folder = os.path.join(output_base_folder, filename[:-4])  # Remove the .pdf extension for folder name

        # Create the directory if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Convert PDF to images
        images = convert_from_path(pdf_path)

        # Save each image as JPEG in the output folder
        for i, image in enumerate(images):
            image.save(os.path.join(output_folder, f'page_{i+1}.jpeg'), 'JPEG')
