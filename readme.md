API for competition of predictions about FC Zenit's matches 

Registration:
POST| "localhost:9090/registration"
in body:
 - user: <your name> (must be unique)
 - password: <your password>
In case of succes you get token

token has a limit live time about 3600 sec (one hour)
so you can get new token:
POST| "localhost:9090/new_token"
in body:
 - user: <your name>
 - password: <your password>
 In case of succes you get new token

Do your prediction:
POST| "localhost:9090/post_predictions"
in headers:
 - user: <your name>
 - access_token: <your token>
in body of request you must transfer next data in json format:
 - scores: final score of match

Get all of your predictions:
GET| "localhost:9090/get_predictions"
in headers:
 - user: <your name>
 - access_token: <your token>
 
In case of errors you get answer in json format with error description

In project uses next DB:
 - MongoDB.Atlas
 - PostgreSQL 12
