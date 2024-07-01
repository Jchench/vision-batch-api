library(pdftools)

# Create a new folder
output_folder <- "extracted_text"
if (!dir.exists(output_folder)) {
  dir.create(output_folder)
}

# Load the PDF file
pdf_file <- "pdf_1/PL107_204.pdf"

# Extract text from each page
text <- pdf_text(pdf_file)

# Combine all the text into one string
combined_text <- paste(text, collapse = "\n")

# Save the combined text into a single file
output_file <- file.path(output_folder, "extracted_text.txt")
writeLines(combined_text, con = output_file)
