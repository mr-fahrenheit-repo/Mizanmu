# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import socket
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

    for x in range(0,total_product + 20,20):
        # Configuring webdriver render
        url = url + str(x)
        driver.set_window_size(1280,720)
        driver.get(url)

        # Getting plain page source
        content = driver.page_source
        driver.quit()

        # Getting the product link from page
        soup = BeautifulSoup(content, 'html.parser')
        lists = soup.find_all('div', class_= "ms-product-item pull-center")
        for x in lists:
            for a in x('a', href=True):
                productlinks.add(a["href"])
                print("Total product links :", len(productlinks))
            
    productlinks = list(productlinks)
    return productlinks