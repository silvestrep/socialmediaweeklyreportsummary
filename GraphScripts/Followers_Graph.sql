select
 'Instagram' as SocialMedia,
 max(nr_of_followers_thisweek) as Total_Followers,
Max(nr_of_followers_thisweek) - max(nr_of_followers_weekago) as Incremental_followers,
 max(LatestWeek) as Last_Event,
 IFNULL(max(WeekAgo),"0") as Last_Event_TimeAgo
from
(select
*,
case when WeekAgo = eventdatetime then followers end as nr_of_followers_weekago,
case when LatestWeek = eventdatetime then followers end as  nr_of_followers_thisweek
from
(select
a.username,
a.followers,
date(a.eventdatetime) as eventdatetime
, b.LatestWeek , b.WeekAgo
from InstagramStore.InstagramFollowers a 
inner join 
(select 
username,
Max(date(eventdatetime)) as LatestWeek,
DATE_SUB(Max(date(eventdatetime)), INTERVAL 7 DAY) as WeekAgo
 from InstagramStore.InstagramFollowers
where username = 'padrehimalaya'
)b on date(a.eventdatetime) in (LatestWeek,WeekAgo) and a.username = b.username)a
)b
union 
select
 'Soundcloud' as SocialMedia,
max(z.total_followers) as Total_Followers,
max(z.total_followers) - max(z.total_followers_timeago) as Incremental_Followers,
max(z.last_eventdate) as Last_Event,
IFNULL(max(z.last_eventdate_timeago),"0") as Last_Event_TimeAgo
from(
select

case when date(a.eventdatetime) = b.LatestWeek then followers end as total_followers,
case when date(a.eventdatetime) = b.WeekAgo then followers end as total_followers_timeago,
case when date(a.eventdatetime) = b.LatestWeek then date(eventdatetime) end as last_eventdate,
case when date(a.eventdatetime) = b.WeekAgo then date(eventdatetime) end as last_eventdate_timeago
from soundcloudstore.users a 
inner join 
(select
Max(date(eventdatetime)) as LatestWeek,
DATE_SUB(Max(date(eventdatetime)), INTERVAL 7 DAY) as WeekAgo
, userid
from soundcloudstore.users
group by userid
)b
on date(a.eventdatetime) in (LatestWeek,WeekAgo) and a.userid = b.userid
where a.userid = '110652450'
)z
union 
select
'Twitter' as SocialMedia,
max(z.total_followers) as Total_Followers,
max(z.total_followers) - max(z.total_followers_timeago) as Incremental_Followers,
max(z.last_eventdate) as Last_Event,
IFNULL(max(z.last_eventdate_timeago),"0") as Last_Event_TimeAgo
from(
select
case when date(a.eventdatetime) = b.latestevent then followers end as total_followers,
case when date(a.eventdatetime) = b.latesteventweekago then followers end as total_followers_timeago,
case when date(a.eventdatetime) = b.latestevent then date(eventdatetime) end as last_eventdate,
case when date(a.eventdatetime) = b.latesteventweekago then date(eventdatetime) end as last_eventdate_timeago
from twitterstore.twitterfollowers a 
inner join 
(select
max(date(eventdatetime)) as latestevent
,IFNULL(DATE_SUB(Max(date(eventdatetime)), INTERVAL 7 DAY),"0") as latesteventweekago, username
from twitterstore.twitterfollowers
group by username
)b
on a.username = b.username and date(a.eventdatetime) = b.latestevent or date(a.eventdatetime) = b.latesteventweekago
where a.username = 'padrehimalaya'
)z
