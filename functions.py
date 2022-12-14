import re
import colorama
from bs4 import BeautifulSoup

# Removing blank spaces from text
def striping(text):
    text = text.strip()
    return text
    
# removing special character from digit
def number_plain(text):
    text = re.sub(r'[-()\"#/@;:<>{}`+=~|*.!?,]','', text).strip()
    text = text.replace("Rp", "")
    text = int(text)
    return text

# removing other than alphabet
def clean_text(text):
    text = re.sub(r'[-()\"#/@;:<>{}`+=~|*.!?,]','', text).strip()
    return text
    
# removing underscore from text
def remove_under(text):
    x = text.replace("_", " ")
    return x
# Removing unknown characters
def remove_unknown(text):
    text = text.encode('ascii', 'ignore')
    text = text.decode('utf-8')
    text = text.strip()
    return text

# Finding the link in string
def find_link(text):
    link = BeautifulSoup(text, "html.parser")
    link = link.find_all("img")
    for img in link:
        img_link = img["src"]
    return img_link

# photo_links = []
# final_photo_links = []
# photo = soup.find_all('div', class_="item text-center")
# for x in photo:
#     lil = x.find_all("img")
#     for y in lil:
#         photo_links.append(y['src'])
# for x in photo_links:
#     if x not in final_photo_links:
#         print(x)
#         final_photo_links.append(x)

# Removing text from string
def numbers(text):
    x = re.sub("\D", "", text)
    return int(x)

# Getting only numbers from string
def list_numbers(text):
    x = re.findall(r'\d+', text)
    return x

# Making progress bar 
def progress_bar(progress, total, color = colorama.Fore.YELLOW):
    percent = 100 * (progress / float(total))
    bar = "█" * int(percent) +  "-" * (100 - int(percent))
    print(color + f"\r|{bar}| {percent:.2f}%", end="\r")
    if progress >= total:
        print(colorama.Fore.GREEN + f"\r|{bar}| {percent:.2f}%", end="\r")
        print(colorama.Fore.RESET)
        
def get_number(text):
    temp = re.findall(r'\d+', text)
    numb = temp[0]
    return int(numb)