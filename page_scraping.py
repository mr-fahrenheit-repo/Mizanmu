# Importing libraries
from config import chromedriver
from config import url
from config import total_product
from Scraping_product_link import get_links

# Getting product links
product_links = get_links(url, total_product)

print(product_links)