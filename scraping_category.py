# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import socket
import requests
from config import chromedriver
from functions import progress_bar
import time

def get_category(url):
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
    
    # List of element to be scrape
    kategori_list = []
    nama_kategori = []

    # Getting the product link from page
    soup = BeautifulSoup(content, 'html.parser')
    sub_menu = soup.find('div', class_="col-lg-3 col-md-4 pull-left pull-none")
    list_sub = sub_menu.find('div', id="list_sub_kategories")
    list_kat = list_sub.find_all('a',href=True)
    
    # Assiging progress bar for monitoring progress
    progress_bar(0, len(list_kat))
    
    for i,x in enumerate(list_kat):
        kategori_list.append(x['href'])
        nama_kategori.append(x.text)
        progress_bar(i + 1, len(list_kat))
    del kategori_list[0]
    del nama_kategori[0]
    print("Total product category :",len(kategori_list))
    list_elements = [nama_kategori, kategori_list]
    return list_elements