from bs4 import BeautifulSoup
import requests
import pprint
import sendemail
import datetime as dt
import time

res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')

# beautifulSoup converts from String to a Python object (parsing)
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.storylink')
links2 = soup2.select('.storylink')
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtext = subtext + subtext2

def prettytext(content):
	final = ''
	for i in content:
		final = final + i['title'] + '\n' + str(i['votes']) + '\n' + i['link'] + '\n'
		final = final + '\n'
	return final

# sort list of news
def sort_stories_by_votes(hnlist):
	return sorted(hnlist, key= lambda k: k['votes'], reverse=True)

# make list of posts above 100 points and return top 5
def create_custom_hn(links, subtext):
	hn = []
	for index, item in enumerate(links):
		title = links[index].getText()
		href = links[index].get('href', None)
		vote = subtext[index].select('.score')
		if len(vote):
			points = int(vote[0].getText().split(' ')[0])
			if (points > 100):
				hn.append({'title': title, 'link':href, 'votes':points})
	return sort_stories_by_votes(hn)[:5]

# pprint.pprint(create_custom_hn(mega_links, mega_subtext))
content = prettytext(create_custom_hn(mega_links, mega_subtext))

first_email_time = dt.datetime(2020, 8, 21, 19, 50, 0)
interval = dt.timedelta(days=1)

send_time = first_email_time
def send_email_at(send_time):
	time.sleep(send_time.timestamp() - time.time())
	sendemail.send_email_to('danielbenet986@gmail.com', content)
	print('email sent!')

try:
	while True:
		send_email_at(send_time)
		send_time = send_time + interval
		time.sleep(10)
except KeyboardInterrupt: 
		print('stopping')

