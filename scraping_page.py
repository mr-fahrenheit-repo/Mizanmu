# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import random
from random import randint
import socket
import requests
from config import chromedriver
from functions import remove_unknown
from functions import number_plain
from functions import list_numbers
from functions import get_number
from functions import numbers
from functions import progress_bar

def get_database(product_links):
    list_judul = []
    list_harga_retail = [] 
    list_harga_diskon = [] 
    list_deskripsi = []
    list_penerbit = []
    list_penulis = []
    list_isbn = []
    list_berat = []
    list_panjang = []
    list_lebar = []
    list_tinggi = []
    list_halaman = []
    list_cover = []
    list_stok = []
    list_description_length = []
    list_link_produk = []
    list_bahasa = []
    list_merek = []
    list_link_foto = []
    
    # Configuring socket for scraping
    socket.getaddrinfo('localhost', 8080)
    
    # Configuring webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('extensionLoadTimeout', 60000)
    service = Service(chromedriver)
    driver = webdriver.Chrome(service = service, options= chrome_options)
    driver.set_window_size(1280,720)
    
    # Assiging progress bar for monitoring progress
    progress_bar(0, len(product_links))
    
    # Looping each link
    for i,plink in enumerate(product_links):
        progress_bar(i + 1, len(product_links))
        url = plink
        
        # Configuring webdriver render
        driver.get(url)
        
        # Getting the page source
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        
        # check stock
        try:
            check = soup.find("div", class_="single-product-detail")
            check_stock = check.find('span', class_="availability").text.split()
        except:
            check_stock = "habis"
        
        if check_stock[2] == "Tersedia":
            
            # collecting product title
            try:
                judul = remove_unknown(soup.find("span", id="tag_judul").text)
            except:
                judul = "undefined"
              
            # collecting product price
            try:
                harga_retail = number_plain(soup.find('strong', class_="harga-discount").text)
            except:
                harga_retail = 0
                
            # collecting product price
            try:
                harga_diskon = number_plain(soup.find('strong', style="color:#ff8401;").text)
            except:
                try:
                    harga_diskon = number_plain(soup.find('div', class_="rating-and-price-2").text)
                except:
                    harga_diskon = 0

            # collecting product description 
            try :    
                deskripsi = remove_unknown(soup.find('div', class_="description p-margin").text)
            except :
                deskripsi = "undefined"
                
            # collecting product's publshier information    
            try:
                penerbit = remove_unknown(soup.find('strong', style="color:#ff8401; margin-left:5px;").text)
            except:
                penerbit = "undefined"
                
            # Collecting product's author information 
            try:
                pengarang = remove_unknown(soup.find('strong', style="color:#ff8401; margin-right:5px;").text)
            except:
                pengarang = "undefined"
            
            # fetching raw detail information of product
                
            try:  
                table = []
                table_parent = soup.find("div", id="tab-3")
                trs = table_parent.find_all("tr")
            except:
                pass
            else:
                for tr in trs:
                    tds = tr.find_all('td')
                    for td in tds:
                        table.append(td.text)
                    
            # convert list into dictionary
            table = table[2:]
            key = table[::2]
            value = table[1::2]
            detail = dict(zip(key, value))
            
            rand_list=[]
            for i in range(7):
                rand_list.append(random.randint(0,9))
            # Converting integer list to string list
            s = [str(i) for i in rand_list]
            # Join list items using join()
            res = "".join(s)    

            # collecting product's ISBN
            try:
                isbn = numbers(detail.get('ISBN'))
            except:
                isbn = "978602" +  res
                isbn = int(isbn)
            else:
                if isbn == 0:
                    isbn = "978602" +  res
                    isbn = int(isbn)

            # collecting product's weight information
            try:
                berat = get_number(detail.get('Berat'))
            except:
                berat = "undefined"
                
            try:
                dimensi = list_numbers(detail.get("Dimensi (P/L/T)"))
            except:
                panjang = randint(13, 15)
                lebar = randint(19, 21)
                tinggi = randint(1,3)
            else:
                try:
                    panjang = int(dimensi[0])
                except:
                    panjang = randint(13, 15)
                try:
                    lebar = int(dimensi[1])
                except:
                    lebar = randint(19, 21)
                try:
                    tinggi = int(dimensi[2])
                except:
                    tinggi = randint(1,3)
                else:
                    if tinggi == 0:
                        tinggi = randint(1,3)
                        
                
            # collecting prouduct's page
            try: 
                halaman = get_number(detail.get('Halaman'))
            except:
                halaman = berat * 0.9
          
            # collecting product's cover information
            try:
                jenis_cover = detail.get("Jenis Cover")
            except:
                jenis_cover = "undefined"
            
            if jenis_cover == "":
                jenis_cover = "Soft Cover"

            # adding more information to the deskcription
            ## adding product's specification    
            info = ""
            for x in range(len(detail)):
                info += list(detail.keys())[x].strip()
                info += " : "
                info += list(detail.values())[x].strip()
                info += "\n"

            ## adding store's branding and information to description
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


            # checking and assigning description length
            if len(deskripsi) < 2999:
                description_length = "under"
            else:
                description_length = "over"

            # Adding product's link webpage    
            link_product = url

            # Collecting product's link image
            photo_link = []
            try: 
                foto = soup.find('div', class_="col-lg-4 col-md-5 col-sm-12")
            except:
                link_foto ="undefined"
            else:
                pl = foto.find_all("img")
                for y in pl:
                    photo_link.append(y['src'])
                    
            link_foto = photo_link[0]
            
            merek = 0
            bahasa = "Indonesia"
            stok = 9
            
            
            list_judul.append(judul)
            list_harga_retail.append(harga_retail) 
            list_harga_diskon.append(harga_diskon) 
            list_deskripsi.append(deskripsi)
            list_penerbit.append(penerbit)
            list_penulis.append(pengarang)
            list_isbn.append(isbn)
            list_berat.append(berat)
            list_panjang.append(panjang)
            list_lebar.append(lebar)
            list_tinggi.append(tinggi)
            list_halaman.append(halaman)
            list_cover.append(jenis_cover)
            list_merek.append(merek)
            list_bahasa.append(bahasa)
            list_stok.append(stok)
            list_description_length.append(description_length)
            list_link_produk.append(link_product)
            list_link_foto.append(link_foto)
        else:
            pass
        
                
    # Creating dictionary form collected product's information
    data = {
        "judul buku" : list_judul,
        "harga retail" : list_harga_retail,
        "harga diskon" : list_harga_diskon,
        "deskripsi" : list_deskripsi,
        "ISBN" : list_isbn,
        "berat" : list_berat,
        "panjang" : list_panjang,
        "lebar" : list_lebar,
        "tinggi" : list_tinggi,
        "halaman" : list_halaman,
        "cover" : list_cover,
        "penerbit" : list_penerbit,
        "penulis" : list_penulis,
        "link produk" : list_link_produk,
        "link foto" : list_link_foto,
        "merek" : list_merek,
        "stok" : list_stok,
        "bahasa" : list_bahasa,
        "panjang deskripsi" : list_description_length
    }
    return data