from pdf2image import convert_from_path
import os

# Path to the PDF file
pdf_path = 'pdf_1/PL110_343.pdf'

# Path to the directory where images will be saved
output_folder = 'PL110_343'

# Create the directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Convert PDF to images
images = convert_from_path(pdf_path)

# Save each image as JPEG or PNG in the output folder
for i, image in enumerate(images):
    image.save(os.path.join(output_folder, f'page_{i+1}.jpeg'), 'JPEG') 
