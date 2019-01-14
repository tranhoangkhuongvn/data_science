
# coding: utf-8

# In[1]:


from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from time import time
from random import randint
from warnings import warn
from IPython.core.display import clear_output


# In[2]:


url = 'https://www.domain.com.au/sale/?excludeunderoffer=1&ssubs=1&postcode='


# In[3]:


#pc_df = pd.read_csv('pclist.csv')


# In[4]:


#pc_list = pc_df['postcode'].tolist()
postal_codes = [2040, 2450, 2430, 2753, 2640, 2795, 2444, 2148, 2750, 2570, 2483, 2620, 2540, 2460, 2618, 2515, 2113, 2787, 2440, 2328, 2470, 3644, 2099, 2880, 2780, 2484, 2161, 2360, 2536, 2250, 2166, 2575, 2722, 2560, 2428, 2000, 2739, 2140, 2340, 2229, 2311, 2756, 2261, 2325, 2456, 2535, 2529, 2574, 2330, 2320, 2566, 2775]


# In[5]:


#len(postal_codes)


# In[6]:


page_number_ls = [str(i) for i in range(1,51)]
for item in postal_codes:
    url += (str(item) + ',')

url += '&page='
print(url)
agent_brands = []
ls_property_address = []
property_prices = []
property_types = []
bedrooms = []
bathrooms = []
carparks = []
land_areas = []
requests = 0
#start_time = time()


# In[7]:


start_time = time()
for page in page_number_ls:
    response = get(url + page)
    sleep(randint(8,15))
    requests += 1
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait=True)

    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, requests/elapsed_time))
    if requests > 50:
        warn('Number of requests was greater than expected.')
        break

    html_soup = BeautifulSoup(response.text, 'html.parser')

    listing_container = html_soup.find('div', class_='search-results__main')
    try:
        property_list = listing_container.find_all('li', attrs={"class": ['search-results__topspot', 'search-results__listing']})
    except:
        continue

    print('No. property per page: ',len(property_list))
    for estate in property_list:
        estate_detail = estate.find('link')
        #print(estate_detail)
        if estate_detail is None:
            sub_listing = estate.find_all('a', class_='listing-result__listing')
            for item in sub_listing:
                sub_listing_url = item['href']
                sleep(randint(1,5))
                sub_estate_detail = get(sub_listing_url)
                sub_html_soup = BeautifulSoup(sub_estate_detail.text, 'html.parser')
                try:
                    detail_container = sub_html_soup.find('div', class_='listing-details__summary-title-container')
                except:
                    continue

                try:
                    property_address = detail_container.h1.text
                except:
                    print(estate_detail)
                    property_address = 'N/A'

                try:
                    property_price = detail_container.find('span', class_='listing-details__listing-summary-title-name').text
                except:
                    property_price = 'Contact Agent'


                ls_property_address.append(property_address)
                property_prices.append(property_price)
                property_feature = detail_container.find_all('span', class_='property-feature__feature-text-container')
                try:
                    bedroom = property_feature[0].text
                except:
                    bedroom = 'N/A'

                try:
                    bathroom = property_feature[1].text
                except:
                    bathroom = 'N/A'

                try:
                    parking = property_feature[2].text
                except:
                    parking = 0

                try:
                    area = property_feature[3].text
                except:
                    area = 'N/A'
                print('Price: ', property_price)
                print('Address: ', property_address)
                print('Bedroom: ', bedroom)
                print('Bathroom: ', bathroom)
                print('Parking: ', parking)
                print('Area: ', area)
                bedrooms.append(bedroom)
                bathrooms.append(bathroom)
                carparks.append(parking)
                land_areas.append(area)


        else:

            sub_estate_url = estate_detail['href']
            sub_estate_detail = get(sub_estate_url)
            sub_html_soup = BeautifulSoup(sub_estate_detail.text, 'html.parser')
            try:
                detail_container = sub_html_soup.find('div', class_='listing-details__summary-title-container')
            except:
                continue

            try:
                property_address = detail_container.h1.text
            except:
                print(estate_detail)
                property_address = 'N/A'

            try:
                property_price = detail_container.find('div', class_='listing-details__summary-title').text
            except:
                property_price = 'Contact Agent'


            ls_property_address.append(property_address)
            property_prices.append(property_price)
            property_feature_container = detail_container.find('div', class_='property-features__default-wrapper')
            property_feature = detail_container.find_all('span', class_='property-feature__feature-text-container')
            try:
                bedroom = property_feature[0].text
            except:
                bedroom = 'N/A'

            try:
                bathroom = property_feature[1].text
            except:
                bathroom = 'N/A'

            try:
                parking = property_feature[2].text
            except:
                parking = 0

            try:
                area = property_feature[3].text
            except:
                area = 'N/A'

            print('Price: ', property_price)
            print('Address: ', property_address)
            print('Bedroom: ', bedroom)
            print('Bathroom: ', bathroom)
            print('Parking: ', parking)
            print('Area: ', area)
            bedrooms.append(bedroom)
            bathrooms.append(bathroom)
            carparks.append(parking)
            land_areas.append(area)

domain_listing = pd.DataFrame({'Address': ls_property_address,
							   'Price': property_prices,
							   'Bedroom': bedrooms,
							   'Bathroom': bathrooms,
							   'Carpark': carparks,
							   'Area': land_areas})

print(domain_listing.info())
domain_listing.to_csv('domains_listing.csv')
