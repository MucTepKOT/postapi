import pymongo
import logging

log_format = '%(asctime)s %(filename)s: %(message)s'
logging.basicConfig(filename="server.log", format=log_format, level=logging.DEBUG)

def connect_mongo():
    try:
        mongo_atlas = "mongodb+srv://muctepkot:pass@kot-elknu.gcp.mongodb.net/test?retryWrites=true&w=majority"
        client = pymongo.MongoClient(mongo_atlas)
        client.admin.command('ismaster')
        logging.info('MongoDB connected')
    except pymongo.errors.OperationFailure as err:
        logging.warning(f'MONGO DB connection error: {str(err)}')
        return str(err)
    db = client.mongodb
    return db

def update_db(db, collection, **kwargs):
    try:
        connect_collection = db[collection]
        connect_collection.find_one_and_update({'user_name': kwargs['user_name'], 'fixture_id': kwargs['fixture_id']}, {"$set": kwargs}, upsert=True)
        return None
    except pymongo.errors.PyMongoError as err:
        return f'Here is some error: {str(err)}'

def my_prediction(db, collection, user):
    try:
        connect_collection = db[collection]
        db_answer = connect_collection.find({'user_name' : user}, {'_id': False})
        return list(db_answer)
    except pymongo.errors.PyMongoError as err:
        return f'Here is some error: {str(err)}'

def check_time_prediction(db, collection, timestamp):
    try:
        connect_collection = db[collection]
        db_answer = connect_collection.find({'elapsed': 0}, {'_id': False})
    except pymongo.errors.PyMongoError as err:
        return f'Here is some error: {str(err)}'
    future_matches = list(db_answer)
    next_match = future_matches[0]
    match_datetime = next_match['event_timestamp']
    timedelta = match_datetime - timestamp
    if timedelta >= 600 and timedelta <= 86400:
        return next_match['fixture_id']
    else:
        return 'Error'

def find_all(db, collection):
    connect_collection = db[collection]
    db_answer = connect_collection.find({}, {"_id": False})
    return list(db_answer)