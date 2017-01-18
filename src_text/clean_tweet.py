import pandas as pd
import numpy as np
import os
import nltk
import time
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords # Import the stop word list
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import opinion_lexicon

def tokeniz_english_tweet(df_en):
	#tokenize the tweets
	tknzr = TweetTokenizer(strip_handles=True)
	main_tk = []
	for index, row in df_en.iterrows():
		mt = tknzr.tokenize(row.main)
		main_tk.append(mt)

	df_en['main_tk'] = main_tk
	
	return df_en


def  clean_english_text(df_en):
	
	df_en = tokeniz_english_tweet(df_en)
	
	#add stop words
	stops = set(stopwords.words("english"))
	stops.update(['.', '\'tis', 'twas', 'able', 'across', 'ain\'t', 'almost', 'also', 'among', 'aren\'t', 
              'can\'t', 'cannot', 'could', 'could\'ve', 'couldn\'t', 'didn\'t', 'doesn\'t', 'don\'t', 
              'hasn\'t', 'he\'d', 'he\'ll', 'he\'s', 'how\'d', 'how\'ll', 'how\'s', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 
              'isn\'t', 'it\'s', 'said', 'say', 'says', 'shan\'t', 'she\'d', 'she\'ll', 'she\'s', 'that\'ll', 'that\'s',
              'there\'s', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'wasn\'t', 'we\'d', 'we\'ll', 'we\'re', 
              'weren\'t', 'what\'d', 'what\'s', 'when\'d', 'when\'ll', 'when\'s', 'where', 'where\'d', 'where\'ll',
              'where\'s', 'who\'d', 'who\'ll', 'who\'s', 'why\'d', 'why\'ll', 'why\'s', 'won\'t', 
              'would\'ve', 'wouldn\'t', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 
              '4', 'u', '2', '2b', 'b4', 'b4n', 'bb', 'brb'])
	lemma = WordNetLemmatizer()
	stemmer = LancasterStemmer()
	meaningful_main = []
	#remove stop words, lemmatize and stemmerize 
	for tweet in df_en.main_tk:
		meaningful_tweet = [w for w in tweet if not w in stops]
		lemmatized_tweet = [lemma.lemmatize(w) for w in meaningful_tweet]
		stemmer_tweet = [stemmer.stem(w) for w in lemmatized_tweet]
		meaningful_main.append(stemmer_tweet)

	df_en['meaningful_main'] = meaningful_main

	return df_en


def liu_hu_lexicon_polarity(lex_dic, tokens): 
    polarity_score = (sum(lex_dic[w] for w in tokens if w in lex_dic))/(len(tokens)+0.0001)
    return polarity_score

def create_lex_dic():
	pos_words = opinion_lexicon.positive()
	neg_words = opinion_lexicon.negative()
	pos_scores = [1.0000]*len(pos_words)
	neg_scores = [-1.0000]*len(neg_words)
	words = pos_words + neg_words
	scores = pos_scores + neg_scores
    
	lex_dic = dict(zip(words, scores))

	return lex_dic


def set_english_sentiment_scores(df_en):
	
	start_time = time.time()
	#use the clean data
	df_en = clean_english_text(df_en)
	lex_dic = create_lex_dic()
	polarity = []
	for tweet in df_en.meaningful_main:
		score = liu_hu_lexicon_polarity(lex_dic, tweet)
		polarity.append(score)
	
	df_en['clean_main_polarity'] = polarity
	print("--- clean main polarity: %s seconds ---" % (time.time() - start_time))


	start_time = time.time()
	#use the vader analyzer on the raw data
	vader_analyzer = SentimentIntensityAnalyzer()
	polarity = []
	for tweet in df_en.main:
		score = vader_analyzer.polarity_scores(tweet)['compound']
		polarity.append(score)

	df_en['vader_polarity'] = polarity
	print("--- Vader polarity: %s seconds ---" % (time.time() - start_time))

	return df_en


def read_data(data_path):
	
	json_files = [pos_json for pos_json in os.listdir(data_path) if pos_json.endswith('.json')] #list of json files
	
	df = pd.DataFrame()
	for js in json_files:
		df = df.append(pd.read_json(data_path+js))

	df_en = df[df.lang == 'en']
	df_de = df[df.lang == 'de']
	df_fr = df[df.lang == 'fr']

	print('Percentage of English tweets: ', df_en.size/df.size)
	print('Percentage of German tweets: ', df_de.size/df.size)
	print('Percentage of French tweets: ', df_fr.size/df.size)

	return df, df_en, df_de, df_fr


def main():

	df, df_en, df_de, df_fr = read_data('../data/input_tweets/')
	df_en = set_english_sentiment_scores(df_en)
	df_en.to_csv('../data/output_tweets/sentiment_scored_english_tweets.csv')
	df_de.to_csv('../data/output_tweets/german_tweets.csv')
	df_fr.to_csv('../data/output_tweets/french_tweets.csv')




if __name__ == '__main__':
    main()
