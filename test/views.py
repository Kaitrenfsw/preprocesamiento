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
	# r = requests.get('http://procesamiento/topic')
	# print(r.status_code)

	http = urllib3.PoolManager()
	r = http.request('GET', 'http://procesamiento:8000/topic/')
	print(r.status)
	print(r.data)

	context = {
		'user': "request.user",
		'login_form': "login_form",
		'regist_form': "regist_form",
	}	
	return JsonResponse(context)



def get_data(request):

	# client = MongoClient()
	# db = client.knowledge_base
	# documents = db.raw_data.find({})
	# doc_list = copy.copy(documents)

	#Test data:
	my_json = {"organizations": [], "uuid": "c5a2c958b45f10b8c47936a629a9d3f6cb8da053", "thread": {"social": {"gplus": {"shares": 0}, "pinterest": {"shares": 0}, "vk": {"shares": 0}, "linkedin": {"shares": 0}, "facebook": {"likes": 0, "shares": 0, "comments": 0}, "stumbledupon": {"shares": 0}}, "site_full": "www.prnewswire.com", "main_image": "http://photos.prnewswire.com/prnvar/20070917/AQM011LOGO", "site_section": "http://www.prnewswire.com/rss/business-technology/internet-technology-news.rss", "section_title": "PR Newswire: Internet Technology", "url": "http://www.prnewswire.com/news-releases/portland-trail-blazers-score-big-on-season-ticket-renewals-with-marketo-300146244.html", "country": "US", "title": "Portland Trail Blazers Score Big on Season Ticket Renewals", "performance_score": 0, "site": "prnewswire.com", "participants_count": 1, "title_full": "Portland Trail Blazers Score Big on Season Ticket Renewals", "spam_score": 0.0, "site_type": "news", "published": "2015-09-22T21:23:00.000+03:00", "replies_count": 0, "uuid": "c5a2c958b45f10b8c47936a629a9d3f6cb8da053"}, "author": "Marketo", "url": "http://www.prnewswire.com/news-releases/portland-trail-blazers-score-big-on-season-ticket-renewals-with-marketo-300146244.html", "ord_in_thread": 0, "title": "Portland Trail Blazers Score Big on Season Ticket Renewals", "locations": [], "entities": {"persons": [], "locations": [], "organizations": []}, "highlightText": "", "language": "english", "persons": [], "text": "SAN MATEO, Calif. The Portland Trail Blazers are partnering with Marketo to increase game attendance and build deeper, more personalized relationships with fans. Since implementing the platform, the NBA team has converted more fans into season ticket holders and increased overall customer engagement. Leveraging Marketo, the franchise has achieved several all-time organizational records:\nBoosted season ticket renewals by 8 percent (96 percent renewal rate) Increased single game ticket sales by 30 percent Improved email open rates by 45 percent Prior to using Marketo, the team sent generic communications to its fans. From people who had never attended a live event to die-hard Trail Blazers fans, the organization was unable to tailor messages based on different interests. The team's management group needed a system that would help attract people to its arena (Moda Center) for home basketball games as well as concerts, family shows and other special events.\nThe Trail Blazers realized they needed technology that would provide a 360-degree view of their fans. After examining different marketing platforms and technologies, the team selected Marketo for its array of features, easy integration with the organization's sales platform, and intuitive interface. Marketo's extensive analytics provided the team with the information it needed to align the right message to the right fan at the right time.\nBy engaging fans using Marketo, the Trail Blazers improved season ticket renewals to 96 percent – a new franchise record – and increased single game ticket sales by 30 percent. While Portland is the 22 nd -largest NBA market, the Trail Blazers now rank among the league's leaders in fan attendance. The organization also increased the number of fans engaging with their digital content, which promoted other events outside of basketball games.\n\"Marketo allowed us to become smarter marketers because we now understand our fans on a deeper level,\" said Vincent Ircandia , Senior Vice President of Business Operations for the Portland Trail Blazers. \"One of our biggest goals is to build life-long fans, and Marketo has been instrumental in helping us learn more about our customers' needs and how to strategically build a relationship with them over the course of time.\"\nAbout The Portland Trail Blazers\nMembers of the National Basketball Association (NBA), the Portland Trail Blazers were founded in 1970 and purchased by Paul G. Allen in 1988. The team's rich heritage includes 31 playoff appearances, three trips to the NBA Finals, an NBA championship in 1977 and a commitment to community service and sustainability. With a corporate mission to make it better in the community, the Trail Blazers strive to help children and their families throughout Oregon and Southwest Washington live, learn and play. The Trail Blazers are the first and only professional sports franchise to receive the prestigious National Points of Light Award for excellence in corporate and community service. The Trail Blazers home arena, the Moda Center, earned LEED Gold Recertification in 2015 after becoming the first existing professional sports venue in the world to receive LEED Gold status in 2010. The team is also one of the founding members of the Green Sports Alliance. For more information, visit www.trailblazers.com .\nAbout Marketo\nMarketo (NASDAQ: MKTO ) provides the leading marketing software and solutions designed to help marketers master the art and science of digital marketing. Through a unique combination of innovation and expertise, Marketo is focused solely on helping marketers keep pace in an ever-changing digital world. Spanning today's digital, social, mobile and offline channels, Marketo's Engagement Marketing Platform powers a set of breakthrough marketing automation and marketing management applications to help marketers tackle all aspects of digital marketing from the planning and orchestration of marketing activities to the delivery of personalized interactions that can be optimized in real-time. Marketo's applications are known for their ease-of-use, and are complemented by the Marketing Nation®, a thriving network of more than 450 third-party solutions through our LaunchPoint® ecosystem and over 50,000 marketers who share and learn from each other to grow their collective marketing expertise. The result for modern marketers is unprecedented agility and superior results. Headquartered in San Mateo, CA with offices in Europe , Australia and Japan , Marketo serves as a strategic marketing partner to more than 4,100 large enterprises and fast-growing small companies across a wide variety of industries. For more information, visit www.marketo.com .\nLogo - http://photos.prnewswire.com/prnh/20070917/AQM011LOGO\nSOURCE Marketo", "external_links": ["http://www.nba.com/blazers/", "http://studio-5.financialcontent.com/prnews?Page=Quote&Ticker=MKTO", "http://www.marketo.com/", "http://www.trailblazers.com/"], "published": "2015-09-22T21:23:00.000+03:00", "crawled": "2015-09-22T16:23:51.096+03:00", "highlightTitle": ""}
	text = my_json["text"]
	words = nltk.word_tokenize(text)

	# Pre-processing the list of words and lemmatize it
	words = pre_processing_text(words)
	lemmas = lemmatize_verbs(words)

	# Transform to text separate by spaces
	text = " ".join(lemmas)
	my_json["text"] = text
	new_json = {"documents": [my_json]}
	json_data = json.dumps(new_json)
	pprint(json_data)
	http = urllib3.PoolManager()
	r = http.request('PUT', 'http://procesamiento:8000/ldamodel/', body=json_data, headers={'Content-Type': 'application/json'})

	# corpus = []
	# i=1

	# for document in doc_list:
	# 	# Creat a copy of document that can be modify
	# 	new_doc = document

	# 	# Get the text body of the document and tokenize it
	# 	text = new_doc["text"]
	# 	words = nltk.word_tokenize(text)

	# 	# Pre-processing the list of words and lemmatize it
	# 	words = pre_processing_text(words)
	# 	lemmas = lemmatize_verbs(words)

	# 	# Transform to text separate by spaces
	# 	text = " ".join(lemmas)
	# 	new_doc["text"] = text

	# 	# Add new document to corpus
	# 	corpus.append(new_doc)
	# 	print(str(i)+" Done!")
	# 	i = i + 1


	# Test prints
	# pprint(documents[0])
	# pprint(corpus[0])
	
	# Save Corpus in a MongoDB Collection
	# save_corpus = db.corpus.insert_many(corpus)


	# Send corpus to API with POST request, using request library:
	# r = requests.post('host', data = corpus)

	return JsonResponse({"respose": "JSON enviado"})





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

#Remove verbs from tokenized list of words
def remove_verbs(words):
	tagged = nltk.pos_tag(words)
	new_words = []
	for tag_word in tagged:
		if not tag_word[1].startswith('V'):
			new_words.append(tag_word[0])

	return new_words

#Remove numbers from tokenized list of words (full digit words only)
def remove_numbers(words):
	new_words = []
	for word in words:
		if not word.isdigit():
			new_words.append(word)

	return new_words

#Execute all the preprocessing steps in a list of tokenized words.
def pre_processing_text(words):
	words = remove_non_ascii(words)
	words = to_lowercase(words)
	words = remove_punctuation(words)
	words = remove_stopwords(words)
	words = remove_verbs(words)
	words = remove_numbers(words)
	return words