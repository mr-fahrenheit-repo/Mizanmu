import re

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
    
# Removing unknown characters
def remove_unknown(text):
    text = text.encode('ascii', 'ignore')
    text = text.decode('utf-8')
    text = text.strip()
    return text

# Finding the link in string
def find_link(text):
    link = text
    try:
        link = link[link.find('http'):link.find('.jpg') + 4]
    except:
        link = link[link.find('http'):link.find('.png') + 4]
    return link

# Removing text from string
def numbers(text):
    x = re.sub("\D", "", text)
    return int(x)
# Getting only numbers from string
def list_numbers(text):
    x = re.findall(r'\d+', text)
    return x