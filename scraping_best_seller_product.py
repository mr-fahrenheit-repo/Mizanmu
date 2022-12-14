# importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import socket
import time 
import re
import pandas as pd
from config import chromedriver
from functions import progress_bar

def get_best_seller(list_link):
    nama_produk = []
    jumlah_terjual = []
    toko = []
    
    
    for link in list_link:
        url_index = link.find("0")
        url = link
        nama = url[url.find("id/")+3 : url.find("?")]
        print(f"Collecting data from {nama}")
        progress_bar(0, 9)
        for x in range(0,9):
            url_temp = list(url)
            url_temp[url_index] = str(x)
            url = "".join(url_temp)
          
            # Configuring socket for scraping
            socket.getaddrinfo('localhost', 8080)

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            service = Service(chromedriver)
            driver = webdriver.Chrome(service = service, options= chrome_options)

            # Configuring webdriver render
            driver.set_window_size(1280,720)
            driver.get(url)
            time.sleep(20) 
            driver.execute_script("window.scrollTo(0, 50000)")
            time.sleep(20)

            # requesting the url
            content = driver.page_source

            # Configuring beautiful soup for scraping
            soup = BeautifulSoup(content, 'html.parser')

            product_view = soup.find('div', class_="shop-search-result-view")
            product_list = product_view.find_all('div', class_="shop-search-result-view__item col-xs-2-4")
            nama = url[url.find("id/")+3 : url.find("?")]

            for i in product_list:
                judul = i.find('div', class_="_3Gla5X _2j2K92 _3j20V6").text
                try:
                    terjual = i.find('div', class_="_2Tc7Qg _2R-Crv").text
                except:
                    terjual = "0"
                nama_produk.append(judul)
                jumlah_terjual.append(terjual)
                toko.append(nama)
                
            progress_bar(x + 1, 9)
    
    judul_buku = []

    for x in nama_produk:
        y = x
        y = y.replace("(Boardbook)", "")
        y = y.replace("Boardbook", "")
        y = y.replace("(Buku Anak)", "")
        y = y.replace("[Mizan]", "")
        y = re.sub(r'[-()\"#/@;:<>{}`+=~|*.!?,]','', y)
        y = y.replace("[Mizan Yogyakarta]", "")
        y = y.encode('ascii', 'ignore')
        y = y.decode('utf-8')
        y = y.upper()
        y = y.replace("  ", " ")
        y = y.strip()
        judul_buku.append(y)
        
    terjual = []

    for x in jumlah_terjual:
        y = x
        y = y.replace("RB+", "001")
        y = y.replace("Terjual/ Bulan", "")
        y = y.strip()
        try:
            y = int(y)
        except:
            y = 0
        terjual.append(y)
        
    detail = list(zip(judul_buku, terjual, toko))
    df = pd.DataFrame(detail, columns=['Nama produk', 'Produk terjual / bulan', "Toko Shopee"])
    df = df.dropna()
    df = df.sort_values(by=['Produk terjual / bulan'], ascending=False)
    return df