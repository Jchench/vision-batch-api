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
    "# should" = count_should,
    "# may" = count_may,
    "# should not" = count_should_not,
    "# may not" = count_may_not,
    "# should in gpt" = count_should_B,
    "# may in gpt" = count_may_B,
    "# should not in gpt" = count_should_not_B,
    "# may not in gpt" = count_may_not_B
  )
  
  assign(paste0(law_name, "_word_count"), word_count, envir = .GlobalEnv)
  
  save(word_count, file = paste0("results/", law_name, "_word_count.rda"))
  
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
  accuracy_embed <- tibble(
    law = law_name,
    embed = proportionA_not_in_B,
    gpt = proportionB_not_in_A
  )
  
  assign(paste0(law_name, "_accuracy"), accuracy_embed, envir = .GlobalEnv)
  
  save(accuracy_embed, file = paste0("results/", law_name, "_accuracy.rda"))
  
  # Get examples of 10-grams unique to each document
  unique_to_A <- setdiff(setA, setB)
  unique_to_B <- setdiff(setB, setA)
  
  # Print a few examples
  cat("\nExamples of 10-grams in document A but not in document B:\n")
  print(head(unique_to_A, 10))
  
  cat("\nExamples of 10-grams in document B but not in document A:\n")
  print(head(unique_to_B, 10))
  
}

# List of document pairs and law names
document_pairs <- list(
  list("extracted_text/extracted_PL107_204.txt", "clean/PL107_204_results/PL107_204.txt", "PL107_204")
)

# Process each document pair
for (pair in document_pairs) {
  process_documents(pair[[1]], pair[[2]], pair[[3]])
}
