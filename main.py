# Importing libraries
from config import total_product
from config import shopee
from config import sudut_buku_folder
from config import cat_list
from config import name_list
import pandas as pd
from scraping_product_link import get_links
from scraping_page import get_database
import colorama

print(colorama.Fore.RESET)

print("Script running")

# getting product category links
print("Getting product category links")

for num, link in enumerate(cat_list):
    name = name_list[num]
    print(f"Collecting link from category : {name}")
    # Getting product links
    product_links = get_links(link, total_product)
    
    # print status
    print("Total product links :", len(product_links))
    
    # Print status 
    print(f"Collecting detail from each link")
    
    # making dataframe from product links
    df = pd.DataFrame(get_database(product_links))
    link_foto_blank = df.loc[df['link foto'] == "https://static.mizanmu.id/d/img/book/cover/"]
    desc_over = df.loc[df["panjang deskripsi"] == "over"]
    df.drop(link_foto_blank.index, inplace=True)
    df.drop(desc_over.index, inplace=True)
    
    # Shopee Mass upload Template
    shopee_df = pd.read_excel(shopee)
    shopee_df['Nama Produk']= df['judul buku']
    shopee_df['Harga']= df['harga diskon']
    shopee_df["Stok"] = df["stok"]
    shopee_df['Deskripsi Produk']= df['deskripsi']
    shopee_df['ISBN']= df['ISBN']
    shopee_df['Berat']= df['berat']
    shopee_df['Panjang']= df['panjang']
    shopee_df['Lebar']= df['lebar']
    shopee_df['Tinggi']= df['tinggi']
    shopee_df['Jenis Cover']= df['cover']
    shopee_df['Perusahaan Penerbit']= df['penerbit']
    shopee_df['Foto Sampul']= df['link foto']
    shopee_df['Merek'] = df['merek']
    shopee_df['Bahasa'] = df['bahasa']
    shopee_df['Foto Produk 1']= df['link foto']
    
    # # # Filtering the database
    # # print("Filtering Database")
    # # shopee_df_filetered = filtering(shopee_df,best_seller)

    # Export dataframe to excel
    print("Exporting Database")
    df.to_excel(sudut_buku_folder + "\\" + f"{name}.xlsx")
    shopee_df.to_excel(sudut_buku_folder + "\\" + f"{name}_shopee template.xlsx")