from database.sql import SQLiteDatabaseConnection
from database.sql_models.users_sql_db_model import UsersSQLDBModel


def list_users_sql():
    db = SQLiteDatabaseConnection()
    with db:
        user_list = UsersSQLDBModel.serialize_list(db.list_all_users())
        if not user_list:
            return 404, "No users has been found in DB!"
    return 200, user_list


def get_user_sql(user_id):
    db = SQLiteDatabaseConnection()
    with db:
        user_from_db = db.get_user_by_id(user_id)
        if not user_from_db:
            return 404, f"User with id : {user_id} has not been found in DB!"
        else:
            user_from_db = user_from_db.serialize()
    return 200, user_from_db

# TODO: add delete_user_sql, update_user_sql si create_user_sql