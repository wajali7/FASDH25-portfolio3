# dataframes
This is the folder containing the dataframes deriving data from the articles in the articles directory. Some of these dataframes are large and should not be opened in excel. They are intended to be filtered and visualised using python.

There are three main folders, each created using different methods:

## length

Dataframes here give the length of articles in the corpus:

*length.csv* - each row  corresponds to the length of one article in the corpus, for every article in the corpus\
*length-year.csv* - each row is the total number of words and the mean number of words for the articles in each year\
*length-year-month.csv* - each row is the total number of words and the mean number of words for articles in each month\

## n-grams

n-gram freqencies have been have been calculated for uni-grams (1-gram), bi-grams (2-gram), and tri-grams (3-gram) for the whole corpus. A subdirectory contains csvs relating to each of these n-gram frequencies, with csvs as follows (where n is equal to 1, 2, or 3 depending on the subdirectory):

*n-gram.csv* - frequencies for every n-gram in the corpus with no filtering. Each row corresponds to the number of times that n-gram is mentioned in a specific article\
*n-gram-year.csv* - frequencies for every n-gram grouped by year. Each row counts the number of times an n-gram is mentioned across the articles for that year, and the mean number of mentions of the n-gram for articles across that year\
*n-gram-year-month.csv* - frequencies for every n-gram groups by year and month. Each row counts the number of times an n-gram is mentioned across the articles for that year and month, and the mean number of mentions of the n-gram for articles across that year\

## tfidf

Pairwise files for pairs of articles in the corpus with their tfidf cosine similarity scores. tfidf scores were calculated using sklearn's TfidfVectorizer. To reduce the amount of data, the dataframes only contain article pairs that have a cosine similarity greater than 0.3. Across the files there is metadata for each side of the pairing. E.g. title-1 is the article title for filename-1 and title-2 is the article title for filename-2. There are three csvs with different levels of filtering:

*tfidf-over-0.3.csv* - all pairs of articles with a cosine similarity above 0.3\
*tfidf-over-0.3-len100.csv* - all pairs of articles that are longer than 100 tokens with a similarity score above 0.3\
*tfidf-over-0.3-len200.csv* - all pairs of articles that are longer than 200 tokens with a similarity score above 0.3\

## title

The titles of the articles with their date of pubication and length. This directory contains one csv:

*title.csv* - each row corresponds to an article, with its date of publication and length

## topic-model

A topic moodel of the article corpus created using Python's BERTopic library, with embeddings calculated using the model: all-MiniLM-L6-v2, a sequence length of 512 and nearest neighbours of 15. This directory contains one csv:

*topic-model.csv* - each row corresponds to an article, with a topic number, the number of articles in that topic and 4 topic keywords. Topic -1 is the outlier topic (it means that BERTopic was unable to cluster those articles into a meaningful topic)

## Column names

There are some column names that are common across the dataset (although not all columns are found in each dataframe - use df.columns to get a full list of columns for any of the dataframes):

*year* - the year in which the article was published\
*month* - the month in which the article was published\
*day* - the date of the month the article was published\
*file* or *filename* - the name of the file in the articles folder used to produce that data\
*title* - the title of the article, found above the splitter "\n+-----" in each article\
