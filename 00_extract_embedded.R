library(pdftools)

# Create a new folder
output_folder <- "extracted_text"
if (!dir.exists(output_folder)) {
  dir.create(output_folder)
}

# Set the input folder containing the PDF files
input_folder <- "pdf"

# Get the list of all PDF files in the input folder
pdf_files <- list.files(input_folder, pattern = "\\.pdf$", full.names = TRUE)

# Process each PDF file
for (pdf_file in pdf_files) {
  # Extract text from each page
  text <- pdf_text(pdf_file)
  
  # Combine all the text into one string
  combined_text <- paste(text, collapse = "\n")
  
  # Create the output file name by replacing the .pdf extension with .txt
  output_file <- file.path(output_folder, paste0(tools::file_path_sans_ext(basename(pdf_file)), ".txt"))
  
  # Save the combined text into a single file
  writeLines(combined_text, con = output_file)
}
