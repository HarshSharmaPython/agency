from http import client
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')

db=client['har']
collection=db['userX']

# dict1={'name':'darshan','age':1}#--- insert one
# collection.insert_one(dict1)



# dict2=[{'name':'darshan','age':1},{'name':'kavi','age':4}]#-- insert many
# collection.insert_many(dict2)

db.userY.insert_one({'name':'tani','age':12})