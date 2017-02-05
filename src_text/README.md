# Sentiment Analysis
In this part, we took the tweets in the three languages: English, German and French. Clean_tweet.py takes the path of the data, and analyze the polarity of these tweets.
For each language, we have the following pipeline:

- Tokenize the tweets (we choose the emoticons as a token).
- Remove stop words and punctuations in the tweets.
- Lemmatize and Stemmerize the tweets.
- Create a lexical dictionary and update it with emoticons dictionary.
- Give the polarity point to the tweets based on the dictionary.

For each language we use the following resources:

English:
- TweetTokenizer from nltk. 
- Stop words from nltk corpus. 
- Use WordNetLemmatizer, and LancasterStemmer. 
- Use opinion_lexicon dictionary from nltk.

German:
- Use textblob_de as a tokenizer.
- Stop words from nltk corpus.
- Use SentiWS_v1 dictionary.

French:
- TweetTokenizer from nltk. 
- Stop words from nltk corpus.
- Use senticnet as a dictionary. 
