from requests import get 
from bs4 import BeautifulSoup
import pandas as pd 

url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'

response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')
print(type(html_soup))
#print(response.text[:500])
movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')
print(type(movie_containers))
print(len(movie_containers))

first_movie = movie_containers[0]
print(first_movie.h3.a.text)

first_movie_year = first_movie.h3.find('span', class_='lister-item-year text-muted unbold')
print(first_movie_year.text)

first_movie_rating = first_movie.find('div', class_='inline-block ratings-imdb-rating')
print(first_movie_rating.strong.text)


#first_movie_meta_score= first_movie.find('div', class_='inline-block ratings-metascore')
#print(first_movie_meta_score.span.text)
first_movie_meta_score= first_movie.find('span', class_='metascore favorable')
print(first_movie_meta_score.text)

first_movie_vote = first_movie.find('span', attrs = {'name': 'nv'})
print(first_movie_vote['data-value'])


example_movie = movie_containers[22].find('div', class_ = 'ratings-metascore')
print(type(example_movie))


names = []
years = []
imdb_ratings = []
metascores = []
votes = []

#Extract data from individual movie container
for container in movie_containers:
	if container.find('div', class_='ratings-metascore') is not None:
		name = container.h3.a.text
		names.append(name)

		year = container.h3.find('span', class_='lister-item-year').text
		years.append(year)

		imdb = float(container.strong.text)
		imdb_ratings.append(imdb)

		m_score = container.find('span', class_='metascore').text
		metascores.append(int(m_score))

		vote = container.find('span', attrs = {'name': 'nv'})['data-value']
		votes.append(int(vote))


test_df = pd.DataFrame({'movie': names,
						'year' : years,
						'imdb' : imdb_ratings,
						'metascore' : metascores,
						'votes' : votes
						})

print(test_df.info())
print(test_df.head())
