import pymongo
from datetime import datetime

def insert_db(data):
    try:
        pred_id = pred.insert_one(data).inserted_id
        return pred_id        
    except errors.PyMongoError as e:
        return e

try:
    client = pymongo.MongoClient("mongodb+srv://muctepkot:pass@kot-elknu.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = client.mongodb
    pred = db.predictions
    # print(pred.find_one())
    # print(pred.count_documents({}))
    print('Database connected')
except errors.PyMongoError as e:
    print(e)

data = {'username':'Ornold', 'scores': '5-3'}
timestamp = datetime.timestamp(datetime.now())
data['timestamp'] = int(timestamp)
# print(insert_db(data))