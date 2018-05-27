from django.shortcuts import render
from django.http import JsonResponse
import json
import re, string, unicodedata, copy
import nltk
import contractions
import json
import os
import pymongo
import request
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from pprint import pprint
from pymongo import MongoClient


import urllib3# Create your views here.

def test(param):
	context = {
		'user': "request.user",
		'login_form': "login_form",
		'regist_form': "regist_form",
	}	
	return JsonResponse(context)


def get_data(request):

	client = MongoClient()
	db = client.knowledge_base
	documents = db.raw_data.find({})
	doc_list = copy.copy(documents)

	corpus = []
	i=1

	for document in doc_list:
		# Creat a copy of document that can be modify
		new_doc = document

		# Get the text body of the document and tokenize it
		text = new_doc["text"]
		words = nltk.word_tokenize(text)

		# Pre-processing the list of words and lemmatize it
		words = pre_processing_text(words)
		lemmas = lemmatize_verbs(words)

		# Transform to text separate by spaces
		text = " ".join(lemmas)
		new_doc["text"] = text

		# Add new document to corpus
		corpus.append(new_doc)
		print(str(i)+" Done!")
		i = i + 1


	# Test prints
	pprint(documents[0])
	pprint(corpus[0])
	
	# Save Corpus in a MongoDB Collection
	save_corpus = db.corpus.insert_many(corpus)


	# Send corpus to API with POST request, using request library:
	# r = requests.post('host', data = corpus)

	return JsonResponse(context)	




#Function definitios

#Set the prefix number when searching files in a dataset.
def set_prefix_num(file_num):
	prefix = ''
	if file_num < 10:
		prefix = '000000'
	elif file_num < 100:
		prefix = '00000'
	elif file_num < 1000:
		prefix = '0000'
	elif file_num < 10000:
		prefix = '000'
	elif file_num < 100000:
		prefix = '00'
	elif file_num < 1000000:
		prefix = '0'

	return prefix

#Remove non ASCII words from a tokenized list.
def remove_non_ascii(words):
	new_words = []
	for word in words:
		new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
		new_words.append(new_word)
	return new_words

#Transform all words in a tokenized list to lowercase.
def to_lowercase(words):
	new_words = []
	for word in words:
		new_word = word.lower()
		new_words.append(new_word)
	return new_words

#Reove punctuation from a list of tokenized words.
def remove_punctuation(words):
	new_words = []
	for word in words:
		new_word = re.sub(r'[^\w\s]', '', word)
		if new_word != '':
			new_words.append(new_word)
	return new_words

#Remove stop words from list of tokenized words.
def remove_stopwords(words):
	new_words = []
	for word in words:
		if word not in stopwords.words('english'):
			new_words.append(word)
	return new_words

#Stem words in list of tokenized words
def stem_words(words):
	stemmer = LancasterStemmer()
	stems = []
	for word in words:
		stem = stemmer.stem(word)
		stems.append(stem)
	return stems

#Lemmatize verbs in list of tokenized words
def lemmatize_verbs(words):
	lemmatizer = WordNetLemmatizer()
	lemmas = []
	for word in words:
		lemma = lemmatizer.lemmatize(word, pos='v')
		lemmas.append(lemma)
	return lemmas



#Execute all the preprocessing steps in a list of tokenized words.
def pre_processing_text(words):
	words = remove_non_ascii(words)
	words = to_lowercase(words)
	words = remove_punctuation(words)
	words = remove_stopwords(words)
	return words



def main():

