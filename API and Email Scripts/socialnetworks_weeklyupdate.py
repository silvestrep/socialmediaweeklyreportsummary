
# READ !!!!!! https://stackoverflow.com/questions/8940368/connect-to-two-databases 

import pymysql
import pandas as pd 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

df = pd.read_excel("/Users/joaopimenta/documents/joaopython/EmailScripts/UsersDetails.xlsx",sheet_name='Sheet1')

df = df[["soundcloud_UserId","Instagram_Username","Email_Address","Instagram_Username","TwitterUsername"]] 


df = df.values.tolist()


for x,y,z,s,t in df:


  db_connection = pymysql.connect(user='root', password='joaosoundcloudstore',
                                host='127.0.0.1'
                                #,database='soundcloudstore'
                                )
  x = str(x)
  #x = len(x)
  
  #print(x)

  y = str(y)

  t = str(t)

# SOUNDCLOUD LOGIC 

  if len(x) == 3: # Here I am creating the logic if the cell is empty. For some reason empty cells have a length of 3 
    NoSoundcloudData = True 
  elif len(x) != 3:
    df_soundcloud_followers = pd.read_sql('select max(z.total_followers) as Total_Followers, max(z.total_followers) - max(z.total_followers_timeago) as Incremental_Followers, max(z.last_eventdate) as Last_Event, IFNULL(max(z.last_eventdate_timeago),"0") as Last_Event_TimeAgo from( select case when date(a.eventdatetime) = b.LatestWeek then followers end as total_followers, case when date(a.eventdatetime) = b.WeekAgo then followers end as total_followers_timeago, case when date(a.eventdatetime) = b.LatestWeek then date(eventdatetime) end as last_eventdate, case when date(a.eventdatetime) = b.WeekAgo then date(eventdatetime) end as last_eventdate_timeago from soundcloudstore.users a  inner join  (select Max(date(eventdatetime)) as LatestWeek, DATE_SUB(Max(date(eventdatetime)), INTERVAL 7 DAY) as WeekAgo , userid from soundcloudstore.users group by userid )b on date(a.eventdatetime) in (LatestWeek,WeekAgo) and a.userid = b.userid where a.userid = "%s")z'%(x),con=db_connection)
  else:
    print("Shit got wrong on soundcloud sql query")  

# INSTAGRAM LOGIC 


  if y == "No Data": # Here I am creating a logic if we store "NoData" everytime a user doesn't log an account for a social media platform
    NoInstagramaData = True
  elif y != "No Data":
    df_instagram_followers = pd.read_sql('select max(nr_of_followers_thisweek) as Total_Followers, Max(nr_of_followers_thisweek) - max(nr_of_followers_weekago) as Incremental_followers,  max(LatestWeek) as Last_Event,  IFNULL(max(WeekAgo),"0") as Last_Event_TimeAgo from (select *, case when WeekAgo = eventdatetime then followers end as nr_of_followers_weekago, case when LatestWeek = eventdatetime then followers end as  nr_of_followers_thisweek from (select a.username, a.followers, date(a.eventdatetime) as eventdatetime , b.LatestWeek , b.WeekAgo from InstagramStore.InstagramFollowers a  inner join  (select  username, Max(date(eventdatetime)) as LatestWeek, DATE_SUB(Max(date(eventdatetime)), INTERVAL 7 DAY) as WeekAgo  from InstagramStore.InstagramFollowers where username = "%s")b on date(a.eventdatetime) in (LatestWeek,WeekAgo) and a.username = b.username)a )b'%(y),con=db_connection)
  else: 
    print("Shit got wrong on instagram sql query") 

# TWITTER LOGIC 


  if t == "nan": # Here I am creating a logic if we store "NoData" everytime a user doesn't log an account for a social media platform
    NoTwitterData = True
  elif t != "nan":
    df_Twitter_followers = pd.read_sql('select max(z.total_followers) as Total_Followers, max(z.total_followers) - max(z.total_followers_timeago) as Incremental_Followers, max(z.last_eventdate) as Last_Event, IFNULL(max(z.last_eventdate_timeago),"0") as Last_Event_TimeAgo from( select case when date(a.eventdatetime) = b.latestevent then followers end as total_followers, case when date(a.eventdatetime) = b.latesteventweekago then followers end as total_followers_timeago, case when date(a.eventdatetime) = b.latestevent then date(eventdatetime) end as last_eventdate, case when date(a.eventdatetime) = b.latesteventweekago then date(eventdatetime) end as last_eventdate_timeago from twitterstore.twitterfollowers a  inner join  (select max(date(eventdatetime)) as latestevent ,IFNULL(DATE_SUB(Max(date(eventdatetime)), INTERVAL 7 DAY),"0") as latesteventweekago, username from twitterstore.twitterfollowers group by username )b on a.username = b.username and date(a.eventdatetime) = b.latestevent or date(a.eventdatetime) = b.latesteventweekago where a.username = "%s")z'%(t),con=db_connection)
  else: 
    print("Shit got wrong on Twitter sql query") 

 
  db_connection.close()

  if len(x) == 3:
    bodysoundcloud = "You don't have a Soundcloud Account registered with us"
  elif df_soundcloud_followers.iloc[0, 0] >= 0 and df_soundcloud_followers.iloc[0, 3] == "0": # Means If there is no historical data
    bodysoundcloud = "You have {} followers in Soundcloud. Next week we will tell you how many incremental followers you have".format(df_soundcloud_followers.iloc[0, 0])
  elif ((df_soundcloud_followers.iloc[0, 0] > 0 and df_soundcloud_followers.iloc[0, 1] > 0) and (df_soundcloud_followers.iloc[0, 0] > df_soundcloud_followers.iloc[0, 1])):
    bodysoundcloud = "You have {} followers in Soundcloud. Those are {} more followers in between {} and {}".format(df_soundcloud_followers.iloc[0, 0],df_soundcloud_followers.iloc[0, 1],df_soundcloud_followers.iloc[0, 3],df_soundcloud_followers.iloc[0, 2])
  elif df_soundcloud_followers.iloc[0, 0] >= 0 and df_soundcloud_followers.iloc[0, 1] < 0: # less followers
    bodysoundcloud = "You have {} followers in Soundcloud. Those are {} followers in between {} and {}".format(df_soundcloud_followers.iloc[0, 0],df_soundcloud_followers.iloc[0, 1],df_soundcloud_followers.iloc[0, 3],df_soundcloud_followers.iloc[0, 2])
  elif (df_soundcloud_followers.iloc[0, 0] > 0 and df_soundcloud_followers.iloc[0, 1] == 0) or (df_soundcloud_followers.iloc[0, 0] == 0 and df_soundcloud_followers.iloc[0, 1] == 0):
    bodysoundcloud = "You have {} followers in Soundcloud. You didn't have any more followers between {} and {}".format(df_soundcloud_followers.iloc[0, 0],df_soundcloud_followers.iloc[0, 3],df_soundcloud_followers.iloc[0, 2])
  else: 
    bodysoundcloud = "There is a problem here. We are trying to fix it"

  if y == "nan":
    bodyinstagram = "You don't have an Instagram Account registered with us"
  elif df_instagram_followers.iloc[0, 0] >= 0 and df_instagram_followers.iloc[0, 3] == "0": # Means If there is no historical data
    bodyinstagram = "You have {} followers in Instagram. Next week we will tell you how many incremental followers you have".format(df_instagram_followers.iloc[0, 0])
  elif df_instagram_followers.iloc[0, 0] > 0 and df_instagram_followers.iloc[0, 1] > 0: # more followers
    bodyinstagram = "You have {} followers in Instagram. Those are {} more followers in between {} and {}".format(df_instagram_followers.iloc[0, 0],df_instagram_followers.iloc[0, 1],df_instagram_followers.iloc[0, 3],df_instagram_followers.iloc[0, 2])
  elif df_instagram_followers.iloc[0, 0] >= 0 and df_instagram_followers.iloc[0, 1] < 0: # less followers
    bodyinstagram = "You have {} followers in Instagram. Those are {}  followers in between {} and {}".format(df_instagram_followers.iloc[0, 0],df_instagram_followers.iloc[0, 1],df_instagram_followers.iloc[0, 3],df_instagram_followers.iloc[0, 2])
  elif (df_instagram_followers.iloc[0, 0] > 0 and df_instagram_followers.iloc[0, 1] == 0 and df_instagram_followers.iloc[0, 3] != "0") or (df_instagram_followers.iloc[0, 0] == 0 and df_instagram_followers.iloc[0, 1] == 0 and df_instagram_followers.iloc[0, 3] != "0"):
    bodyinstagram = "You have {} followers in Instagram. You didn't have any more followers between {} and {}".format(df_instagram_followers.iloc[0, 0],df_instagram_followers.iloc[0, 3],df_instagram_followers.iloc[0, 2])
  else: 
    bodyinstagram = "There is a problem here. We are trying to fix it"


  if str(t) == "nan":
    bodytwitter = "You don't have an Twitter Account registered with us"
  elif df_Twitter_followers.iloc[0, 0] >= 0 and df_Twitter_followers.iloc[0, 3] == "0": # Means If there is no historical data
    bodytwitter = "You have {} followers in Twitter. Next week we will tell you how many incremental followers you have".format(df_Twitter_followers.iloc[0, 0])
  elif df_Twitter_followers.iloc[0, 0] > 0 and df_Twitter_followers.iloc[0, 1] > 0:
    bodytwitter = "You have {} followers in Twitter. Those are {} more followers in between {} and {}".format(df_Twitter_followers.iloc[0, 0],df_Twitter_followers.iloc[0, 1],df_Twitter_followers.iloc[0, 3],df_Twitter_followers.iloc[0, 2])
  elif df_Twitter_followers.iloc[0, 0] >= 0 and df_Twitter_followers.iloc[0, 1] < 0: # less followers
    bodytwitter = "You have {} followers in Twitter. Those are {} followers in between {} and {}".format(df_Twitter_followers.iloc[0, 0],df_Twitter_followers.iloc[0, 1],df_Twitter_followers.iloc[0, 3],df_Twitter_followers.iloc[0, 2])
  elif df_Twitter_followers.iloc[0, 0] >= 0 and df_Twitter_followers.iloc[0, 1] == 0 and df_Twitter_followers.iloc[0, 3] != "0":
    bodytwitter = "You have {} followers in Twitter. You didn't have any more followers between {} and {}".format(df_Twitter_followers.iloc[0, 0],df_Twitter_followers.iloc[0, 3],df_Twitter_followers.iloc[0, 2])
  else: 
    bodytwitter = "There is a problem here. We are trying to fix it"

  #if bodyinstagram == "There is a problem here. We are trying to fix it":
    #print(df_instagram_followers)

  email_user = 'XXX@gmail.com' 
  email_password = 'XXX'
  #x = 'jsgpimenta18@gmail.com'


  subject = '%s_DataWeeklyUpdate'%(s)

  msg = MIMEMultipart() # defines a multipart object
  msg['From'] = email_user
  msg['To'] = z
  msg['Subject'] = subject



  message="""\
      <html>
          <head></head>
          <body>
              <b>Soundcloud</b>
              <p>"""+bodysoundcloud+"""</p>
              <b>Instagram</b>
              <p>"""+bodyinstagram+"""</p>
              <b>Twitter</b>
              <p>"""+bodytwitter+"""</p>
          </body>
      </html>
      """

  msg.attach(MIMEText(message,'html'))


  text = msg.as_string() # converts the msg from an object to a plain text string.
  server = smtplib.SMTP('smtp.gmail.com',587) #mail server that we want to use and the port that we want to use. Gmail server is 'smpt.gmail.com' and the port is 587. This might change in the future, we can google it
  server.starttls() #any smtp command after this is going to be encripted to protect my password.
  server.login(email_user,email_password) #Log in to my gmail account


  server.sendmail(email_user,z,text)
  server.quit()









