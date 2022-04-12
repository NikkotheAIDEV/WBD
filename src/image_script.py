from time import sleep
from images.image_search import search_museum
from query import Connection
from models import consts

connection = Connection(consts.HOST, consts.DATABASE, consts.USER, consts.PASSWORD)
connection.startConnection()

query = "SELECT museum_name FROM Museums"
results = connection.query(query)
results = results[2016:] # Move 1 before current

# Move with 1 before current
for index, museum in enumerate(results, 2016):
    print("\n\n\n" + str(index+1))
    
    img = search_museum(museum[0])
    img1 = img["image_1"]
    thumb1 = img["thumbnail_1"]

    query_insert_img = "UPDATE Museums SET image_url = %s WHERE id = %s"
    query_insert_thumb = "UPDATE Museums SET thumbnail_url = %s WHERE id = %s"
    
    tuple1 = (str(img1), str(index+1))
    tuple2 = (str(thumb1), str(index+1))

    connection.insert_prepared_statement(query_insert_img, tuple1)
    connection.insert_prepared_statement(query_insert_thumb, tuple2)

# print(results[0])
# test = search_museum(results[0])
# print(test)

connection.stopConnection()