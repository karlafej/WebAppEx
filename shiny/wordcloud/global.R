library(tm)
library(wordcloud)
library(memoise)
library(capek)

# The list of valid books
books <<- list("Továrna na absolutno" = "tovarna_na_absolutno",
              "Krakatit" = "krakatit",
              "Hordubal" = "hordubal",
              "Povětroň"="povetron",
              "Obyčejný život"="obycejny_zivot",
              "Válka s mloky"="valka_s_mloky")

stopwords_cs <<- read.csv("stopwords-cs.txt", header=FALSE, encoding = "UTF-8", as.is=TRUE)[,1]

# Using "memoise" to automatically cache the results
getTermMatrix <- memoise(function(book) {
  # Careful not to let just any name slip in here; a
  # malicious user could manipulate this value.
  if (!(book %in% books))
    stop("Unknown book")

  text <- get(book) 

  myCorpus = Corpus(VectorSource(text))
  myCorpus = tm_map(myCorpus, content_transformer(tolower))
  myCorpus = tm_map(myCorpus, removePunctuation)
  myCorpus = tm_map(myCorpus, removeNumbers)
  myCorpus = tm_map(myCorpus, removeWords, stopwords_cs) 

  myDTM = TermDocumentMatrix(myCorpus,
              control = list(minWordLength = 1))
  
  m = as.matrix(myDTM)
  
  sort(rowSums(m), decreasing = TRUE)
})
