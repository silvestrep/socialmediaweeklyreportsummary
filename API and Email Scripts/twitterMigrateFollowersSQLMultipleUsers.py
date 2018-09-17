import tweepy
import pandas as pd 
import mysql.connector

consumer_key = 'XXX'
consumer_secret = 'XXX'

access_token = 'XXX-XXX'
access_token_secret = 'XXX'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

df = pd.read_excel("/Users/joaopimenta/documents/joaopython/EmailScripts/UsersDetails.xlsx",sheet_name='Sheet1')

df = df.values.tolist()

df = [i[6] for i in df]

dflist = [x for x in df if str(x) != 'nan'] # Removes the nulls. This list will only contain the soundcloud ids from users who have a soundcloud page 



userslist = []

for x in dflist:
	usersdata = api.get_user('%s'%(x))
	userslist.append((usersdata.name,usersdata.followers_count))



conn = mysql.connector.connect(user='root', password='XXX',
                              host='127.0.0.1',
                              database='Twitterstore')

cursor = conn.cursor()

q = """INSERT INTO TwitterFollowers (username, followers) VALUES (%s,%s)"""

cursor.executemany(q, userslist)
conn.commit()



