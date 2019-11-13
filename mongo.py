import pymongo
from datetime import datetime

def insert_db(data):
    try:
        pred_id = pred.insert_one(data).inserted_id
        return pred_id        
    except pymongo.errors.PyMongoError as e:
        return 'Here is some error: %s' % e

try:
    client = pymongo.MongoClient("mongodb+srv://muctepkot:pass@kot-elknu.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = client.mongodb
    pred = db.predictions
    # print(pred.find_one())
    # print(pred.count_documents({}))
    print('Database connected')
except pymongo.errors.PyMongoError as e:
    print('Here is some error: %s' % e)

data = {'username':'Ornold', 'scores': '5-3'}
timestamp = datetime.timestamp(datetime.now())
data['timestamp'] = int(timestamp)
# print(insert_db(data))