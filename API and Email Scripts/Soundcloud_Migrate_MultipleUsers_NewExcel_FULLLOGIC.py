import soundcloud
import pandas as pd 
import mysql.connector
import itertools

client = soundcloud.Client(client_id='XXX')


 
df = pd.read_excel("/Users/joaopimenta/documents/joaopython/EmailScripts/UsersDetails.xlsx",sheet_name='Sheet1')


df = df.values.tolist() # converts dataframe to a list

df = [i[0] for i in df] # for some reason there were square brackets in between each item and this function removes them


dflist = [x for x in df if str(x) != 'nan'] # Removes the nulls. This list will only contain the soundcloud ids from users who have a soundcloud page 


userslist = []


for x in dflist:
	x = int(x)
	usersdata = client.get('/users/%s'%(x))
	userslist.append((usersdata.id,usersdata.followers_count))



conn = mysql.connector.connect(user='root', password='XXX',
                              host='127.0.0.1',
                              database='soundcloudstore')

cursor = conn.cursor()

q = """INSERT INTO Users (userid, followers) VALUES (%s,%s)"""

cursor.executemany(q, userslist)
conn.commit()


trackslist = []


for x in dflist:
	x = int(x)
	tracksdata = client.get('/users/%s/tracks'%(x))
	for x in tracksdata:
		trackslist.append((x.title, str(x.playback_count),str(x.id),str(x.favoritings_count),str(x.comment_count),str(x.user_id)))

conn = mysql.connector.connect(user='root', password='joaosoundcloudstore',
                              host='127.0.0.1',
                              database='soundcloudstore')

cursor = conn.cursor()

q = """INSERT INTO Tracks (Track_Name, Plays,TrackId,Likes,Comments,userid) VALUES (%s,%s,%s,%s,%s,%s)"""

cursor.executemany(q, trackslist)
conn.commit() 


