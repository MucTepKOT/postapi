import pymongo

def connect_mongo():
    mongo_atlas = "mongodb+srv://muctepkot:pass@kot-elknu.gcp.mongodb.net/test?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_atlas)
    return client

def insert_db(db, collections, **kwargs):
    try:
        connect_db = connect_mongo()[db][collections]
        connect_db.insert_one(kwargs).inserted_id
        return 'Success'
    except pymongo.errors.PyMongoError as err:
        return 'Here is some error: %s' % err

def my_prediction(db, collections, user):
    try:
        connect_db = connect_mongo()[db][collections]
        db_answer = connect_db.find({'user_name' : user}, {'_id': False})
        return list(db_answer)
    except pymongo.errors.PyMongoError as err:
        return 'Here is some error: %s' % err
