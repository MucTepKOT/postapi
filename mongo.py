import pymongo

mongo_atlas = "mongodb+srv://muctepkot:pass@kot-elknu.gcp.mongodb.net/test?retryWrites=true&w=majority"

def insert_db(db, collections, **kwargs):
    try:
        client = pymongo.MongoClient(mongo_atlas)
        connect_db = client[db][collections]
        connect_db.insert_one(kwargs).inserted_id
        return 'Success'
    except pymongo.errors.PyMongoError as err:
        return 'Here is some error: %s' % err

def my_prediction(db, collections, user):
    try:
        client = pymongo.MongoClient(mongo_atlas)
        connect_db = client[db][collections]
        db_answer = connect_db.find({'user_name' : user}, {'_id': False})
        return list(db_answer)
    except pymongo.errors.PyMongoError as err:
        return 'Here is some error: %s' % err
