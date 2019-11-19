Registration:
POST| "localhost:9090/registration"
in body:
 - user: <your name> (must be unique)
 - password: <your password>
In case of succes you get token

Do your prediction:
POST| "localhost:9090/post_predictions"
in headers:
 - user: <your name>
 - access_token: <your token>
in body of request you must transfer next data in json format:
 - Players: player(s) who score a goal
 - Scores: final score of match

Get all of your predictions:
GET| "localhost:9090/get_predictions"
in headers:
 - user: <your name>
 - access_token: <your token>
In case of errors you get answer in json format with error description

In project uses next DB:
 - MongoDB.Atlas
 - PostgreSQL 12
