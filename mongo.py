import pymongo

def connect_mongo():
    mongo_atlas = "mongodb+srv://muctepkot:Aegis2018@kot-elknu.gcp.mongodb.net/test?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_atlas)
    return client

def update_db(db, collection, **kwargs):
    try:
        connect_db = connect_mongo()[db][collection]
        connect_db.find_one_and_update({'user_name': kwargs['user_name'], 'fixture_id': kwargs['fixture_id']}, {"$set": kwargs}, upsert=True)
        return 'Success'
    except pymongo.errors.PyMongoError as err:
        return 'Here is some error: %s' % err

def my_prediction(db, collection, user):
    try:
        connect_db = connect_mongo()[db][collection]
        db_answer = connect_db.find({'user_name' : user}, {'_id': False})
        return list(db_answer)
    except pymongo.errors.PyMongoError as err:
        return 'Here is some error: %s' % err

def check_time_prediction(db, collection, timestamp):
    try:
        connect_db = connect_mongo()[db][collection]
        db_answer = connect_db.find({'elapsed': 0}, {'_id': False})
    except pymongo.errors.PyMongoError as err:
        return 'Here is some error: %s' % err
    future_matches = list(db_answer)
    next_match = future_matches[0]
    match_datetime = next_match['event_timestamp']
    timedelta = match_datetime - timestamp
    if timedelta >= 600 and timedelta <= 86400:
        return next_match['fixture_id']
    else:
        return 'Error'

def find_all(db, collection):
    connect_db = connect_mongo()[db][collection]
    db_answer = connect_db.find({}, {"_id": False})
    return list(db_answer)