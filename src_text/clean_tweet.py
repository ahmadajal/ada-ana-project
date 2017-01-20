import pandas as pd
import numpy as np
import string
import re
import os
import nltk
import time
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords # Import the stop word list
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import opinion_lexicon

# German
import textblob_de
from textblob_de import TextBlobDE as TextBlob
from nltk.stem.snowball import GermanStemmer



def tokenize_german_tweet(df_de):
	
	main_tk = []
	for tweet in df_de.main:
		blob_tweet = TextBlob(tweet)
		blob_tweet.tokenizer = textblob_de.tokenizers.PatternTokenizer()
		tk = blob_tweet.tokenizer.tokenize(tweet)
		main_tk.append(tk)

	df_de['main_tk'] = main_tk

	return df_de

def tokeniz_english_tweet(df_en):
	#tokenize the tweets
	tknzr = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
	main_tk = []
	for index, row in df_en.iterrows():
		mt = tknzr.tokenize(row.main)
		main_tk.append(mt)

	df_en['main_tk'] = main_tk
	
	return df_en

def clean_german_text(df_de):

	df_de = tokenize_german_tweet(df_de)

	#add stop words
	stops = set(stopwords.words("german"))
	punctuations = list(string.punctuation)
	stops.update(punctuations)

	#stemmer = GermanStemmer()
	meaningful_main = []
	for tweet in df_de.main_tk:
		meaningful_tweet = [w.lower() for w in tweet if not w.lower() in stops]
		#stemmer_tweet = [stemmer.stem(w) for w in meaningful_tweet]
		meaningful_main.append(meaningful_tweet)

	df_de['meaningful_main'] = meaningful_main
	df_de = df_de.drop('main_tk', axis = 1)

	return df_de

def  clean_english_text(df_en):
	
	df_en = tokeniz_english_tweet(df_en)
	
	#add stop words
	stops = set(stopwords.words("english"))
	stops.update(['\'tis', 'twas', 'able', 'across', 'ain\'t', 'almost', 'also', 'among', 'aren\'t', 
              'can\'t', 'cannot', 'could', 'could\'ve', 'couldn\'t', 'didn\'t', 'doesn\'t', 'don\'t', 
              'hasn\'t', 'he\'d', 'he\'ll', 'he\'s', 'how\'d', 'how\'ll', 'how\'s', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 
              'isn\'t', 'it\'s', 'said', 'say', 'says', 'shan\'t', 'she\'d', 'she\'ll', 'she\'s', 'that\'ll', 'that\'s',
              'there\'s', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'wasn\'t', 'we\'d', 'we\'ll', 'we\'re', 
              'weren\'t', 'what\'d', 'what\'s', 'when\'d', 'when\'ll', 'when\'s', 'where', 'where\'d', 'where\'ll',
              'where\'s', 'who\'d', 'who\'ll', 'who\'s', 'why\'d', 'why\'ll', 'why\'s', 'won\'t', 
              'would\'ve', 'wouldn\'t', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 
              '4', 'u', '2', '2b', 'b4', 'b4n', 'bb', 'brb'])
	punctuations = list(string.punctuation)
	stops.update(punctuations)
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
	df_en = df_en.drop('main_tk', axis = 1)

	return df_en


def liu_hu_lexicon_polarity(lex_dic, tokens): 
    polarity_score = (sum(lex_dic[w] for w in tokens if w in lex_dic))/(len(tokens)+0.0001)  

    polarity_score = 1 if polarity_score >= 1 else (-1 if polarity_score <= -1 else polarity_score)
    return polarity_score 

def list_of_emoticons():

	pos_emoticons = list([':)', ':-)', ':o)', ':]', ':3', 
					':c)', ':>', '=]', '8)', '=)', 
					':}', ':^)', '<3', '^-^', '^^', 
					';)', ';>', '(:', '(;', ':d', 
					':p', ':-p', '>:d<', '>>:d<<', 
					':x', '=))', '8->', ':-*', ':*', 
					'b-)', 'b)', 'o:)', ':o)', '<:-p', 
					'<:p', '\\:d/', 'x-d', 'lol', 
					':\'d', ':\'-d', 'lmao', 'rofl', 
					'roflmao', 'giggle', ':\{\}',';;)', 
					';;-)', 'l-)', 'l)', '=d>', ':)>-', 
					'$-)', '$)', '*-*' ])

	neg_emoticons = list([':(', ':-(', ':<', ':-<', ':[', 
						':-[', ':c', ':-c', ':{', ':/', 
						':\'(' , '[-(', '=((', '>:p', 
						'l-)', ':-&', ':-s', ':s', ':&', 
						'>:p', 'x(',':-w', ':w', 't-t', 't_t', 
						':o', ':-o', ':@', ':-@'])

	return pos_emoticons, neg_emoticons


def create_german_lex_dic():
	
	pos_de = pd.read_csv('../SentiWS_v1.8c/SentiWS_v1.8c_Positive.txt', sep='\t|\|' )
	neg_de = pd.read_csv('../SentiWS_v1.8c/SentiWS_v1.8c_Negative.txt', sep='\t|\|' )


	pos_de.columns = ['word', 'tag', 'score', 'similar_words']
	neg_de.columns = ['word', 'tag', 'score', 'similar_words']
	word_de = pos_de 
	word_de = pos_de.append(neg_de)

	de_dic = dict()
	for index, row in word_de.iterrows():
		score = row.score
		word = row.word.lower()
		if(word in de_dic):
			de_dic[word] = (de_dic[word] + score)/2
		else:
			de_dic[word] = score

		if row.similar_words != None:
			similar_words = str(row.similar_words)
			split_words = re.split(',', similar_words)
			for w in split_words:
				if(w.lower() in de_dic):
					de_dic[w.lower()] = (de_dic[w.lower()] + score)/2
				else:
					de_dic[w.lower()] = score


	pos_emoticons, neg_emoticons = list_of_emoticons() 
	pos_scores = [3.0000]*len(pos_emoticons)
	neg_scores = [-3.0000]*len(neg_emoticons)

	de_dic.update(dict(zip((pos_emoticons+neg_emoticons), (pos_scores+neg_scores))))

	return de_dic

def create_english_lex_dic():
	

	pos_words = opinion_lexicon.positive()
	neg_words = opinion_lexicon.negative()

	pos_emoticons, neg_emoticons = list_of_emoticons() 

	pos_scores = [1.0000]*len(pos_words) + [3.0000]*len(pos_emoticons)
	neg_scores = [-1.0000]*len(neg_words) + [-3.0000]*len(neg_emoticons)

	pos_words = list(pos_words) + pos_emoticons
	neg_words = list(neg_words) + neg_emoticons
	words = pos_words + neg_words
	scores = pos_scores + neg_scores
    
	lex_dic = dict(zip(words, scores))

	return lex_dic


def set_german_sentiment_scores(df_de):
	start_time = time.time()

	df_de = clean_german_text(df_de)
	lex_dic = create_german_lex_dic()
	polarity = []
	for tweet in df_de.meaningful_main:
		score = liu_hu_lexicon_polarity(lex_dic, tweet)
		polarity.append(score)
	
	df_de['clean_main_polarity'] = polarity

	df_de = df_de.drop('meaningful_main', axis = 1)
	print("--- clean main German polarity: %s seconds ---" % (time.time() - start_time))

	return df_de


def set_english_sentiment_scores(df_en):
	
	start_time = time.time()
	#use the clean data
	df_en = clean_english_text(df_en)
	lex_dic = create_english_lex_dic()
	polarity = []
	for tweet in df_en.meaningful_main:
		score = liu_hu_lexicon_polarity(lex_dic, tweet)
		polarity.append(score)
	
	df_en['clean_main_polarity'] = polarity
	df_en = df_en.drop('meaningful_main', axis = 1)
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
	df_de = set_german_sentiment_scores(df_de)
	df_de.to_csv('../data/output_tweets/sentiment_scored_german_tweets.csv')
	#df_fr.to_csv('../data/output_tweets/french_tweets.csv')




if __name__ == '__main__':
    main()
