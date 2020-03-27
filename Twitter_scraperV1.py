
''''Quellen: https://bhaskarvk.github.io/2015/01/how-to-use-twitters-search-rest-api-most-effectively./
        https://stackoverflow.com/questions/21308762/avoid-twitter-api-limitation-with-tweepy for Twitter Rate limits'''
import json
import csv
import tweepy
import re
import pandas as pd 
import scrapy 
import csv
from parsel import Selector

"""
INPUTS:
    consumer_key, consumer_secret, access_token, access_token_secret: codes 
    telling twitter that we are authorized to access this data
    hashtag_phrase: the combination of hashtags to search for
OUTPUTS:
    none, simply save the tweet info to a spreadsheet
"""
excelpath = "/Users/stephanbergmann/Documents/GitHub/classData2Dollar/crunchbasescraper/crunchbasescraper/Scraper_190317/Data/"
#Der Dateipfad hinter dem das Excel liegt 
df = pd.read_excel(excelpath + "crunchbase.xlsx")

df["screenname"] = df["Twitter"].str.strip("https://twitter.com/")
url_list = df["screenname"].tolist()
usernames = [x for x in url_list if str(x) != 'nan']

#Twitte Dev Keys einsetzen 
consumer_key = "KfpHKtxOcxFjo70rfTliuooyK"
consumer_secret = "PY2LLVj4JvviFZqKt6nMbuY7bmqraGbt0VgVJopo475nRyj64I"
access_token = "1195034865558859778-5apUTLarkmPU0R5UaQ8PU3pfc5R8kf"
access_token_secret = "rK3daZtYVM7lVMdIm0xQn35fQlZAZt3it8Zlr8KtjsY4c"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name, exclude_replies = True, include_retweets=False,count=50)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	if alltweets:
		oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,exclude_replies = True, include_retweets=False, count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))

	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[screen_name, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

	#write the csv	
	writer.writerows(outtweets)
	
	pass

with open('Startup_test1tweets.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerow(["screen_name","id","created_at","text","favourite_count"])
	if __name__ == '__main__':
	#pass in the username of the account you want to download
		for screen_name in usernames:
			try:
				get_all_tweets(screen_name)
			except tweepy.TweepError:
				print("Command on user unsuccessful, Skip")
