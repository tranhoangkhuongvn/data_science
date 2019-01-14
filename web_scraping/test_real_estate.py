from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from time import time
from random import randint
from warnings import warn
from IPython.core.display import clear_output

agent_brands = []
property_address = []
property_prices = []
property_types = []
bedrooms = []
bathrooms = []
carparks = []
land_areas = []
pages = [str(i) for i in range(1,100)]
#years_url = [str(i) for i in range(2000,2018)]
requests = 0
start_time = time()

for page in pages:
	response = get('https://www.realestate.com.au/buy/in-new+south+wales/list-' + page)
	sleep(randint(8,15))
	requests += 1
	elapsed_time = time() - start_time
	print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
	clear_output(wait=True)
	if response.status_code != 200:
		warn('Request: {}; Status code: {}'.format(requests, requests/elapsed_time))
	if requests > 82:
		warn('Number of requests was greater than expected.')
		break

	html_soup = BeautifulSoup(response.text, 'html.parser')
	real_estate_containers = html_soup.find_all('article', class_= 'results-card residential-card ')
	if len(real_estate_containers) > 1:
		for real_estate in real_estate_containers:
			address= real_estate['aria-label']
			property_address.append(address)
			try:
				brand = real_estate.find('div', class_='branding branding--large ')['aria-label']
			except:
				brand = 'N/A'
			agent_brands.append(brand)
			property_price = real_estate.find('span', class_='property-price ').text
			property_prices.append(property_price)
			
			property_type = real_estate.find('span', class_='residential-card__property-type').text
			property_types.append(property_type)
			
			property_features= real_estate.find_all('li', class_='general-features__feature')
			bedroom = str(0)
			bathroom = str(0)
			carpark = str(0)
			try:
				bedroom = property_features[0]['aria-label']
			except:
				pass
			try:
				bathroom = property_features[1]['aria-label']
			except:
				pass
			try:
				carpark = property_features[2]['aria-label']
			except:
				pass

			bedrooms.append(bedroom)
			bathrooms.append(bathroom)
			carparks.append(carpark)
			try:
				property_size = real_estate.find('div', class_='property-size rui-clearfix')['aria-label']
			except:
				property_size = 'N/A'
			land_areas.append(property_size)
	else:
		pass
real_estate_listings = pd.DataFrame({'Agent': agent_brands,
									 'Address': property_address,
									 'Price': property_prices,
									 'Type': property_types,
									 'No. Bedroom': bedrooms,
									 'No. Bathroom': bathrooms,
									 'No. Carpark': carparks,
									 'Land area': land_areas})

print(real_estate_listings.info())
real_estate_listings.to_csv('real_estate_listing_updated.csv')
