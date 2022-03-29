from bs4 import BeautifulSoup
import requests

def search_url(query):
    url = "https://www.google.com/search?q=" + str(query) + "&source=lnms&tbm=isch"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')
    if len(images) > 1:
        image = images[1]
        return image['src']

# def search_url_2(query):
#     url = "https://www.google.com/search?q=" + str(query) + "&source=lnms&tbm=isch"
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     images = soup.find_all('a', attrs={"jsname":"sTFXNd"})
#     print(images)

url = search_url("museums troyan")
print(url)