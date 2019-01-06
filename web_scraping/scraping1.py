#Web scraping
#import urllib2
import urllib.request
from bs4 import BeautifulSoup

quote_page = 'https://www.realestate.com.au/buy/in-new+south+wales%3b/list-1'
page = urllib.request.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
#name_box = soup.find_all('span', attrs={'class' : 'property-price '})
#name_box = soup.find_all('span', attrs={'class' : ""})
name_box = soup.find_all('span', class_="")
#name = name_box.text.strip()
#print(soup)
#print(name_box)
for tag in name_box:
	print(tag.string)
