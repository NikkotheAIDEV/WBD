# Target table (person_id, category_id)
from src.deep_learning.helper import Helper
from multiprocessing import Array
from src.query import Connection
from src.models import consts

# Create object
helper = Helper()
connection = Connection(consts.HOST, consts.DATABASE, consts.USER, consts.PASSWORD)

for x in range(1, 1001):
    results = []
    person_recommandations = [x]
    fav_category_id = helper.request_fav_id(x)
    interested_in_categories_ids = helper.request_interested_in_id(x)

    recommendation_fav = helper.request_favourite_6(fav_category_id)
    results.append(recommendation_fav)

    if len(interested_in_categories_ids) != 0:
        recommendation_interested_in = helper.request_interested_in_4(interested_in_categories_ids)
        results.append(recommendation_interested_in)
        

    elements = len(results)
    for y in range(6):
        query_insert = "INSERT INTO Target VALUES ({}, {})".format(x, results[0][y])
        connection.insert(query_insert)
    
    if elements > 1:
        for z in range(4):
            query_insert = "INSERT INTO Target VALUES ({}, {})".format(x, results[1][z])
            connection.insert(query_insert)