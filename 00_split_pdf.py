from pdf2image import convert_from_path
import os

# Path to the folder containing PDF files
input_folder = 'pdf'

# List all files in the input folder
pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]

for pdf_file in pdf_files:
    # Path to the PDF file
    pdf_path = os.path.join(input_folder, pdf_file)
    
    # Path to the directory where images will be saved
    output_folder = os.path.join(input_folder, pdf_file[:-4])  # Remove the .pdf extension for folder name

    # Create the directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Save each image as JPEG in the output folder
    for i, image in enumerate(images):
        image.save(os.path.join(output_folder, f'page_{i+1}.jpeg'), 'JPEG')
