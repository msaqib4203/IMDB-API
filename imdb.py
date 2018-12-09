#Dependancies
from bs4 import BeautifulSoup
import requests
import json

def parsePersons(persons):
			
	names = []
	if isinstance(persons,dict):
		names.append(persons['name'])
		return names
		
	for person in persons:
		if person['@type'] == "Person":
			names.append(person['name'])
	return names

def getJSON(html):

	data = {}
	data['id'] =  html.find(attrs={'property':'pageId'})['content']
	data['url'] = 'https://www.imdb.com/title/'+data['id']
	html_json =  html.find(attrs={'type':'application/ld+json'}).text.strip()
	fetchedJson = json.loads(html_json)
	data['poster'] = html.find(attrs={'class':'poster'}).find('img')['src']
	title_wrapper =  html.find(attrs={'class':'title_wrapper'}).text.strip()
	data['title'] = title_wrapper[:title_wrapper.find(')')+1]
	data['rating'] = html.find(itemprop='ratingValue').text
	data['bestRating'] = html.find(itemprop='bestRating').text
	data['votes'] = html.find(itemprop='ratingCount').text
	data['rated'] = fetchedJson['contentRating']
	data['genres'] = fetchedJson['genre']
	data['description'] = fetchedJson['description']
	data['cast'] = parsePersons(fetchedJson['actor'])
	data['writers'] = parsePersons(fetchedJson['creator'])		
	data['directors'] = parsePersons(fetchedJson['director'])	
	json_data = json.dumps(data)
	return json_data
	
def getHTML(url):
	
	response = requests.get(url)
	return BeautifulSoup(response.content,'html.parser')	
	
def getURL(input):
	try:
		if input[0] == 't' and input[1] == 't':
			html = getHTML('http://www.imdb.com/title/'+input+'/')
			
		else:
			html = getHTML('https://www.google.co.in/search?q='+input)
			for cite in html.findAll('cite'):
				if 'imdb.com/title/tt' in cite.text:
					html = getHTML(cite.text)
					break
		return getJSON(html)	
	except Exception as e:
		print e
		return 'Invalid input or Network Error!'
		
	
input = raw_input("Enter IMDB ID or Title: ")
print('Getting information, Please Wait....')
print(getURL(input))
