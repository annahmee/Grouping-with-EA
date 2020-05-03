import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
grouping_db = myclient["grouping"]
user_col=grouping_db['user']
