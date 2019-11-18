import pymongo
from datetime import datetime

def insert_db(user, data):
    timestamp = datetime.timestamp(datetime.now())
    data['timestamp'] = int(timestamp)
    data['user_name'] = user
    try:
        pred.insert_one(data).inserted_id
        return 'Success'        
    except pymongo.errors.PyMongoError as e: 
        return 'Here is some error: %s' % e

def my_prediction(user):
    try:
        db_answer = pred.find({'user_name' : user}, {'_id': False})
        return list(db_answer)
    except pymongo.errors.PyMongoError as e:
        return 'Here is some error: %s' % e

try:
    client = pymongo.MongoClient("mongodb+srv://muctepkot:pass@kot-elknu.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = client.mongodb
    pred = db.predictions
    print('Database connected')
except pymongo.errors.PyMongoError as e:
    print('Here is some error: %s' % e)
