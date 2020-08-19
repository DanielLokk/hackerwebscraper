from bs4 import BeautifulSoup
import requests
import pprint

res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')

print(res2)

# beautifulSoup converts from String to a Python object (parsing)
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.storylink')
links2 = soup2.select('.storylink')
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtext = subtext + subtext2

def sort_stories_by_votes(hnlist):
	return sorted(hnlist, key= lambda k: k['votes'], reverse=True)

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
	return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(mega_links, mega_subtext))