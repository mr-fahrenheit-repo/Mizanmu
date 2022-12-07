# Importing libraries
from config import chromedriver
from config import url
from config import total_product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from Scraping_product_link import get_links
from bs4 import BeautifulSoup
import socket
import time
from functions import remove_unknown
from functions import number_plain
from functions import numbers
from functions import list_numbers

# Getting product links
product_links = get_links(url, total_product)

# Configuring socket for scraping
socket.getaddrinfo('localhost', 8080)

# Configuring selenium webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
service = Service(chromedriver)
driver = webdriver.Chrome(service = service, options= chrome_options)

# Configuring webdriver render
driver.set_window_size(1280,720)
driver.get(url)
time.sleep(1)

content = driver.page_source

# Getting the product link from page
soup = BeautifulSoup(content, 'html.parser')
judul = soup.find('h2', class_= "title-detail").text
tipe = soup.find('button', class_= "btn btn-xs btn-info").text
kategori = soup.find('a', class_= "btn btn-xs btn-info").text
harga = number_plain(soup.find('div', class_="product-price").text)
deskripsi = remove_unknown(soup.find('div', class_="detail-tab-info").text)
detail =  []       
for x in soup.find_all("div", {"class" : "item-toggle-tab"}):
    trs = x.find_all("tr")
    for tr in trs:
        tds = tr.find_all('td')
        for td in tds:
            detail.append(td.text)
            
detail1 = soup.find('div',  {"class" : "col-md-12 col-sm-12 col-xs-12"})
trs = detail1.find_all("tr")
for tr in trs:
    tds = tr.find_all('td')
    for td in tds:
        detail.append(td.text)
            
detail = [x for x in detail if remove_unknown(x)!= ":"]
key = detail[::2]
value = detail[1::2]
detail = dict(zip(key, value))
del detail["SKU"]

isbn = numbers(detail.get('ISBN', "undefined"))
berat = numbers(detail.get('Berat', "undefined"))
dimensi = list_numbers(detail.get('Dimensi (P/L/T)', "undefined"))
panjang = dimensi[0]
lebar = dimensi [1]
tinggi = dimensi[2]
halaman = numbers(detail.get('Halaman', "undefined"))
tahun = numbers(detail.get('Tahun Terbit', "undefined").strip())
cover = detail.get('Jenis Cover', "undefined").strip()
penerbit = detail.get('Penerbit', "undefined")
penulis = detail.get('Penulis', "undefined")

info = ""
for x in range(len(detail)):
    info += list(detail.keys())[x].strip()
    info += " : "
    info += list(detail.values())[x].strip()
    info += "\n"

deskripsi += "\n"
deskripsi += "\n"
deskripsi += "Spesifikasi Buku"
deskripsi += "\n"
deskripsi += "\n"
deskripsi += info
deskripsi += "\n"
deskripsi += "One stop shopping untuk kebutuhan membaca kamu. Menyediakan buku-buku berkualitas dengan harga yang terjangkau."
deskripsi += "\n"
deskripsi += "Jam operasional toko :"
deskripsi += "\n"
deskripsi += "Senin - Sabtu : 08:00 - 18:00 WIB"
deskripsi += "\n"
deskripsi += "\n"
deskripsi += "Pastikan tanyakan stok terlebih dahulu sebelum checkout."
deskripsi += "\n"
deskripsi += "\n"
deskripsi += "#sudutbuku #bukumurah #shoppingbuku"

if len(deskripsi) < 2999:
    description_length = "under"
else:
     description_length = "over"