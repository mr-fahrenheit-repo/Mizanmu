# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import socket
import time
from config import chromedriver

# Configuring socket for scraping
socket.getaddrinfo('localhost', 8080)

# Getting links functions
def get_links(url, total_product):
    # Product link (empty)
    productlinks = set()

    # Configuring selenium webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    service = Service(chromedriver)
    driver = webdriver.Chrome(service = service, options= chrome_options)

    for x in range(0,total_product + 24,24):
        # Configuring webdriver render
        y  = str(x)
        driver.set_window_size(1280,720)
        driver.get(url + y)
        time.sleep(1)

        # Getting plain page source
        content = driver.page_source

        # Getting the product link from page
        soup = BeautifulSoup(content, 'html.parser')
        lists = soup.find_all('div', class_= "ms-product-item pull-center")
        for x in lists:
            for a in x.find_all('a', alt="produk", href=True):
                productlinks.add(a['href'])
        print("Total product links :", len(productlinks))
            
    # productlinks = list(productlinks)
    return productlinks