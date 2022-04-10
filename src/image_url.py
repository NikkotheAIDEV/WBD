from readline import insert_text
from bs4 import BeautifulSoup
from query import Connection
from models import consts
import requests

def search_url(query):
    url = "https://www.google.com/search?q=" + str(query) + "&source=lnms&tbm=isch"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')
    if len(images) > 1:
        image = images[1]
        return image['src']

connection = Connection(consts.HOST, consts.DATABASE, consts.USER, consts.PASSWORD)
connection.startConnection()

query = "SELECT museum_name FROM Museums"
all_museums = connection.query(query)
for index, museum in enumerate(all_museums, start=2879):
    image_url = search_url(museum[0])
    insert_query = "UPDATE Museums SET image_url = \'{}\' WHERE id = {};".format(image_url ,index+1)
    connection.insert_prepared_statement(insert_query, None)
    print(index)

connection.stopConnection()