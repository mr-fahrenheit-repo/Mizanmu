# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import socket
import requests
from config import chromedriver
from functions import progress_bar
from functions import get_number

# Getting links functions
def get_links(url, total_product):
    productlinks = []

    # Configuring socket for scraping
    socket.getaddrinfo('localhost', 8080)

    # Configuring webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(chromedriver)
    driver = webdriver.Chrome(service = service, options= chrome_options)

    # Configuring webdriver render
    driver.set_window_size(1280,720)
    driver.get(url)

    # Getting the page source
    content = driver.page_source

    # Getting the product link from page
    soup = BeautifulSoup(content, 'html.parser')
    check = soup.find('div', class_= "col-md-12 col-sm-12 box-pengarang").text
    check =  get_number(check)

    if check > 0:
    
        # Assiging progress bar for monitoring progress
        progress_bar(0, total_product)
        
        for x in range(0,total_product,20):
            # Configuring webdriver render
            urlx = url + "/" + str(x)
            driver.set_window_size(1280,720)
            driver.get(urlx)
            
            progress_bar(x + 20, total_product)

            # Getting the page source
            content = driver.page_source

            # Getting the product link from page
            soup = BeautifulSoup(content, 'html.parser')
            
            # List of parent links
            lists = soup.find_all('div', class_= "ms-product-item pull-left")
            
            for y in lists:
                link = y.find('a', alt="produk", href=True)
                productlinks.append(link['href'])
                    
    else:
        pass
    new_list = []
    [new_list.append(x) for x in productlinks if x not in new_list]

    return productlinks