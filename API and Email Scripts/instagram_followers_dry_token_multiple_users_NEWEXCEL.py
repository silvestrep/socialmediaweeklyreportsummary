from urllib2 import urlopen

from json import load

import json

import json

import sys

import time

import requests

import mysql.connector

import pandas as pd

df = pd.read_excel("/Users/joaopimenta/documents/joaopython/EmailScripts/UsersDetails.xlsx",sheet_name='Sheet1')


url_list = []



df = df[["Instagram_UserId","Instagram_AccessToken"]] 



df = df.values.tolist()

#dflist = [x for x in df if str(x) != 'nan']

#print(dflist)


for x,y in df:
	if str(x) != 'nan':
		x = int(x)
		url_list.append("https://api.instagram.com/v1/users/%s/?access_token=%s"%(x,y))
	else:
		pass





for x in url_list:

	response=urlopen(x)

	#print(response)

	jsonobj=load(response)
 

	followed = jsonobj["data"]["counts"]["followed_by"]


	name = jsonobj["data"]["username"] 

	data = [name,followed]


	conn = mysql.connector.connect(user='root', password='XXX',
                              host='127.0.0.1',
                              database='InstagramStore')

	cursor = conn.cursor()

	q = """INSERT INTO InstagramFollowers (username,followers) VALUES (%s,%s)"""

	cursor.execute(q, data)
	conn.commit() 

