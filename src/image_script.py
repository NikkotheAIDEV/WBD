from images.image_search import search_museum
from query import Connection
from models import consts

connection = Connection(consts.HOST, consts.DATABASE, consts.USER, consts.PASSWORD)
connection.startConnection()

query = "SELECT museum_name FROM Museums"
results = connection.query(query)

# Move with 1 before current
for index, museum in enumerate(results):
    print("\n\n\n" + str(index+1))
    
    img = search_museum(museum[0])
    if len(img) > 0 and len(img["image_1"]) <= 500:
        img1 = img["image_1"]

        query_insert_img = "UPDATE Museums SET image_url = %s WHERE id = %s"
    
        tuple1 = (str(img1), str(index+1))

        connection.insert_prepared_statement(query_insert_img, tuple1)
    else:
        continue

# print(results[0])
# test = search_museum(results[0])
# print(test)

connection.stopConnection()