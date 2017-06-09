#Dependancies
from bs4 import BeautifulSoup
import urllib2
import json

def getJSON(imdb_id):
	try:
		response = urllib2.urlopen('http://www.imdb.com/title/'+imdb_id+'/')
		html = response.read()
		html = BeautifulSoup(html,'html.parser')
		
	except Exception as e:
		return 'Invalid IMDB ID or Network Error!'
			
	data = {}
	data['poster'] = html.find('img')['src']
	data['title'] =  html.find(itemprop='name').text.strip()
	data['rating'] = html.find(itemprop='ratingValue').text
	data['bestRating'] = html.find(itemprop='bestRating').text
	data['votes'] = html.find(itemprop='ratingCount').text
	data['rated'] = html.find(itemprop='contentRating')['content']
	tags = html.findAll("span",{"itemprop":"genre"})
	genres = []
	for genre in tags:
		genres.append(genre.text.strip())
	data['genre'] = genres	
		
	data['description'] = html.find(itemprop="description").text.strip()

	tags = html.findAll(itemprop="actors")
	actors = []
	for actor in tags:
		actors.append(actor.text.strip().replace(',',''))
	data['cast'] = actors	
		

	tags = html.findAll(itemprop="creator")
	creators = []
	for creator in tags:
		creators.append(creator.text.strip().replace(',',''))
	data['writers'] = creators	
		
	directors = []
	tags = html.findAll(itemprop="director")
	for director in tags:
		directors.append(director.text.strip().replace(',',''))
	data['directors'] = directors	
		
	json_data = json.dumps(data)
	return json_data
	
imdbid = raw_input("Enter IMDB ID: ")
print('Getting information, Please Wait....')
print(getJSON(imdbid))
