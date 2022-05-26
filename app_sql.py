import json

from flask import Flask, request, Response
from database.sql import *
from users.functions_sql import *

app = Flask("Marketplace sql API")


@app.route("/list_users", methods=["GET"])
def list_users():
    status, message = list_users_sql()
    return Response(status=status, response=json.dumps(message))



@app.route("/get_user/<string:user_id>", methods=["GET"])
def get_user(user_id):
    status, message = get_user_sql(user_id)
    return Response(status=status, response=json.dumps(message))


# TODO: implement all the remaining APIs

if __name__ == '__main__':
    db = SQLiteDatabaseConnection()
    with db:
        db.create_tables_if_not_exists()
    app.run()