library(quanteda)
library(tidyverse)

# Function to process a pair of documents
process_documents <- function(doc_path_A, doc_path_B, law_name) {
  # Read and collapse the documents
  documentA <- paste(readLines(doc_path_A), collapse = "\n")
  documentB <- paste(readLines(doc_path_B), collapse = "\n")
  
  # Preprocess the documents
  preprocess <- function(doc) {
    doc <- tolower(doc)
    doc <- gsub("[[:punct:]]", "", doc)
    doc <- gsub("\\s+", " ", doc)
    return(doc)
  }
  
  documentA <- preprocess(documentA)
  documentB <- preprocess(documentB)
  
  # Word count
  count_should <- str_count(documentA, "\\bshould\\b")
  count_may <- str_count(documentA, "\\bmay\\b")
  count_should_not <- str_count(documentA, "\\bshould+not\\b")
  count_may_not <- str_count(documentA, "\\bmay+not\\b")
  
  count_should_B <- str_count(documentB, "\\bshould\\b")
  count_may_B <- str_count(documentB, "\\bmay\\b")
  count_should_not_B <- str_count(documentB, "\\bshould+not\\b")
  count_may_not_B <- str_count(documentB, "\\bmay+not\\b")
  
  # Save word counts
  word_count <- tibble(
    law = law_name,
    "# should in embedd" = count_should,
    "# may in embedd" = count_may,
    "# should not in embedd" = count_should_not,
    "# may not in embedd" = count_may_not,
    "# should in gpt" = count_should_B,
    "# may in gpt" = count_may_B,
    "# should not in gpt" = count_should_not_B,
    "# may not in gpt" = count_may_not_B
  )
  
  # Create tokens for both documents
  tokensA <- tokens(documentA, what = "word")
  tokensB <- tokens(documentB, what = "word")
  
  # Generate 10-grams
  tokensA_10grams <- tokens_ngrams(tokensA, n = 10)
  tokensB_10grams <- tokens_ngrams(tokensB, n = 10)
  
  # Convert tokens to unique sets of 10-grams and eliminate those with numbers
  filter_ngrams <- function(ngrams) {
    ngrams <- unique(as.character(ngrams[[1]]))
    ngrams <- ngrams[!grepl("[0-9]", ngrams)]
    return(ngrams)
  }
  
  setA <- filter_ngrams(tokensA_10grams)
  setB <- filter_ngrams(tokensB_10grams)
  
  # Calculate the proportions
  proportionA_not_in_B <- length(setdiff(setA, setB)) / length(setA)
  proportionB_not_in_A <- length(setdiff(setB, setA)) / length(setB)
  
  # Save the results
  accuracy <- tibble(
    law = law_name,
    embedded_text = proportionA_not_in_B,
    gpt = proportionB_not_in_A
  )
  
  # Get examples of 10-grams unique to each document
  unique_to_A <- setdiff(setA, setB)
  unique_to_B <- setdiff(setB, setA)
  
  # Print a few examples
  cat("\nExamples of 10-grams in document A but not in document B:\n")
  print(head(unique_to_A, 10))
  
  cat("\nExamples of 10-grams in document B but not in document A:\n")
  print(head(unique_to_B, 10))
  
  return(list(word_count = word_count, accuracy = accuracy))
}

# Get the list of files in the embedd_readble and clean/results folders
embedd_files <- list.files("extracted_text", full.names = TRUE)
clean_files <- list.files("clean/results", full.names = TRUE)

# Extract filenames without paths and extensions
embedd_filenames <- basename(embedd_files)
clean_filenames <- basename(clean_files)

# Remove file extensions to match names
embedd_names <- tools::file_path_sans_ext(embedd_filenames)
clean_names <- tools::file_path_sans_ext(clean_filenames)

# Initialize combined tables
combined_word_counts <- tibble()
combined_accuracy <- tibble()

# Process matching pairs of documents
for (i in seq_along(embedd_names)) {
  law_name <- embedd_names[i]
  doc_path_A <- embedd_files[i]
  doc_path_B <- clean_files[which(clean_names == law_name)]
  
  if (length(doc_path_B) == 1) { # Proceed only if a single match is found
    results <- process_documents(doc_path_A, doc_path_B, law_name)
    combined_word_counts <- bind_rows(combined_word_counts, results$word_count)
    combined_accuracy <- bind_rows(combined_accuracy, results$accuracy)
  } else {
    warning(paste("No match or multiple matches found for:", law_name))
  }
}

# Save combined tables
write_csv(combined_word_counts, "results/combined_word_counts_embedd.csv")
write_csv(combined_accuracy, "results/combined_accuracy_embedd.csv")

# Print combined tables
print(combined_word_counts)
print(combined_accuracy)
