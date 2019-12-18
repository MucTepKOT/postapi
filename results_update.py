import requests
import json
import pymongo
from datetime import datetime

''' This programm is for updating matches results and counting user's points, don't forget to configure cron'''


url = 'https://server1.api-football.com/'
token = ''
headers = {'X-RapidAPI-Key': token, 'Accept': 'application/json'}

def all_matches():
    endpoint = 'fixtures/team/596/511'
    try:
        r = requests.get(url+endpoint, headers=headers)
        response = json.loads(r.text)
        return response
    except requests.exceptions.ConnectionError as err:
        print(str(err))
        return 'Error'

def connect_mongo():
    mongo_atlas = "mongodb+srv://muctepkot:Aegis2018@kot-elknu.gcp.mongodb.net/test?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_atlas)
    return client

def insert_db(db, collection, **kwargs):
    try:
        connect_db = connect_mongo()[db][collection]
        connect_db.insert_one(kwargs).inserted_id
        return 'Success'
    except pymongo.errors.PyMongoError as err:
        return 'Here is some error: %s' % err

def drop_collection(db, collection):
    connect_db = connect_mongo()[db]
    connect_db.drop_collection(collection)

def create_collection(db, collection):
    connect_db = connect_mongo()[db]
    connect_db.create_collection(collection)

def collection_init(db, collection):
    all_fixtures = all_matches()['api']['fixtures']
    # drop_collection('mongodb', 'results')
    # create_collection('mongodb', 'results')
    for match in all_fixtures:
        data = {'fixture_id': match['fixture_id'], 'round': match['round'], 'event_timestamp': match['event_timestamp'], 'elapsed': match['elapsed'], 'statusShort': match['statusShort'],'homeTeam': match['homeTeam']['team_name'], 'score': match['score']['fulltime'], 'awayTeam': match['awayTeam']['team_name']}
        match = insert_db(db, collection, **data)
        if match == 'Success':
            return 'OK'
        else:
            return match

def update_fixture(db, collection):
    endpoint = 'fixtures/id/{id}'
    connect_db = connect_mongo()[db][collection]
    db_answer = connect_db.find({'elapsed': 0}, {'_id': False})
    fixture_id = db_answer[0]['fixture_id']
    print(fixture_id)
    endpoint = 'fixtures/id/{0}'.format(fixture_id)
    try:
        r = requests.get(url+endpoint, headers=headers)
        response = json.loads(r.text)
        print(response)
    except requests.exceptions.ConnectionError as err:
        print(str(err))
        print('Error')
    resp_data = response['api']['fixtures'][0]
    try:
        connect_db.find_one_and_update({'fixture_id': fixture_id}, {'$set': {'elapsed': resp_data['elapsed'], 'statusShort': resp_data['statusShort'] , 'score': resp_data['score']['fulltime']}})
        return('DB results successfully updated at {}'.format(datetime.now()))
    except pymongo.errors.PyMongoError as err:
        return str(err)

def get_fixture_id_alter(db, collection):
    connect_db = connect_mongo()[db][collection]
    db_answer = connect_db.find({'elapsed': 90}, {'_id': False})
    return list(db_answer)[-1]

def user_points(db, collection, fixture_id):
    connect_db = connect_mongo()[db][collection]
    db_answer = connect_db.find({'fixture_id': fixture_id}, {'_id': False})
    print(db_answer)
    predictions = []
    for fixture in db_answer:
        predictions.append(fixture)
    return predictions


connect_mongo()
update_result = update_fixture('mongodb', 'results')
print(update_result)
update = get_fixture_id_alter('mongodb', 'results')
print(update)
score = update['score']
fixture_id = update['fixture_id']
predictions = user_points('mongodb', 'predictions', fixture_id)
print(predictions)
for pred in predictions:
    print(pred['scores'], pred['user_name'])
    if score == pred['scores']:
        pts = 5
    else:
        res = int(score[0]) - int(score[2])
        user_res = int(pred['scores'][0]) - int(pred['scores'][2])
        if res > 0 and user_res > 0 or res < 0 and user_res < 0:
            pts = 2
        else:
            pts = 0
    connect_db = connect_mongo()['mongodb']['users_scores']
    connect_db.update_one({'user_name': pred['user_name']}, {'$inc': {'points': pts}}, upsert=True)
    print(pts)
