import re

#access keys
ACCESS_TOKEN = '62108407-zM4ZH0vaUKrRJ5U8KpX5iZHAWNNzb88orn3zHilis'
ACCESS_SECRET = 'puMdX9rKPTxW7YzF9jqQAgmFpzmlWgwG1BinCj6FoauvR'
CONSUMER_KEY = 'QUZcKtPF3TQ0dGgnmCW2H1Bfd'
CONSUMER_SECRET = 'WBW09ApG9CNpvb1ERZIkIgS6TYaZ1nrTeFsc5Y9diZZHxwhJfl'

#query parameters
latitude = 41.4951147	# geographical centre of search
longitude = -81.8459461	# geographical centre of search
max_range = 100			# search range in kilometres
num_results = 100000	# minimum results to obtain
queries = "#lebronjames OR #lebron OR lebron OR @kingjames"
#queries = "#stephencurry OR #curry OR stephen curry OR curry OR steph curry OR @StephenCurry30"
#queries = "#kyrieirving OR #irving OR kyrie irving OR irving OR @KyrieIrving"
#queries = "#cavs OR #cavaliers OR cavs OR cavaliers OR @cavs"
#queries = "#warriors OR #goldenstate OR warriors OR goldenstate OR @cavs"
#database name
db_name = "twitter_"+ re.findall('#(\S+)\s',queries)[0]

day_ago_start, day_ago_end = 3,0

projection = {'user.name':1,"geo":1,"_id":0,'created_at':1,'text':1
              ,'place.full_name':1,'place.country_code':1}
query = {}

