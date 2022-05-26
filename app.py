import json

from flask import Flask, request, Response
from users.functions import create_user_flask, delete_user_flask, update_user_flask, list_users_flask, get_user_flask

app = Flask("Marketplace API")

@app.route('/', methods=["GET"])
def hello_world():
    return f"Welcome to the root page of our marketplace API"


@app.route("/list_users", methods=["GET"])
def list_users():
    list_users = list_users_flask()
    return Response(status=list_users[0], response=json.dumps(list_users[1]))




# TODO: implement the missing APIs for users, products and orders

@app.route('/get_user/<user_id>', methods=["GET"])
def get_user(user_id):
    return get_user_flask(user_id)  # return Response object inside functions module...same thing 


@app.route('/add_user', methods=['POST'])
def add_user():
    post_data = json.loads(request.data)
    status_code, new_user_id = create_user_flask(post_data['name'], post_data['email'])  
    # observatii numele cheilor din post_data sunt hardcodate, pentru asta in programare exista conceptul
    # de model de date si ORM-uri, despre care o sa invatam azi
    return Response(status=status_code, response=new_user_id)


@app.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    status_code, message = delete_user_flask(user_id)
    return Response(status=status_code, response=message)


@app.route('/update_user/<user_id>', methods=['PATCH'])
def update_user(user_id):
    user_data = json.loads(request.data)
    status_code, message = update_user_flask(user_id, user_data)
    return Response(status=status_code, response=message)


## end of methods

if __name__ == '__main__':
    app.run()
