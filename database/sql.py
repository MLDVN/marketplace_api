from functools import wraps

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()  # clasa de baza folosita pentru a crea modele

from database.sql_models.users_sql_db_model import UsersSQLDBModel

import logging
logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(module)s::%(funcName)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("MarketplaceBackend")


def check_session():
    """
    Decorator function to check if the session has been initialized
    :return: callable
    :raises Exception
    """

    def check_session_wrapper(callable_func):
        @wraps(callable_func)
        def decor_inner(instance, *args, **kwargs):
            if not instance.session:
                raise AttributeError('No session. Please use context manager.')
            return callable_func(instance, *args, **kwargs)

        return decor_inner

    return check_session_wrapper


class SQLiteDatabaseConnection:

    def __init__(self):
        self.engine = create_engine("sqlite:///db.sqlite", echo=False)  # engine e un obiect prin care interact. sqlalchemy cu DB
        self.session = None
        self.inspect = sqlalchemy.inspect(self.engine)  # inspect ofera informatii despre obiecte sqlalchemy

    def __enter__(self):  # __enter__ e chemat in momentul in care se intra in context managerul with
        self.session = sessionmaker(bind=self.engine)()  # cream o sesiune pe baza engine`ului

    @check_session()
    def create_tables_if_not_exists(self):
        try:
            if not (self.inspect.has_table(UsersSQLDBModel.__tablename__, schema=None)):
                logger.info(f"Creating table {UsersSQLDBModel.__tablename__}...")
                # loggerul e un mod mai avansat de a da print!!
                try:
                    Base.metadata.create_all(self.engine)  # echivalentul ORM a sql`urilor de creare tabele
                except Exception as ex:
                    logger.error(ex)
                else:
                    logger.info(f"Created table {UsersSQLDBModel.__tablename__}...")
            else:
                logger.info(f"Table {UsersSQLDBModel.__tablename__} already exists!")
        except SQLAlchemyError as e:
            logger.error(e, exc_info=True)
            raise


    @check_session()
    def list_all_users(self):
        """SELECT * FROM Users;"""
        return self.session.query(UsersSQLDBModel).all()
        # django: UsersSQLDBModel.objects.all()


    @check_session()
    def get_user_by_id(self, user_id):
        # SELECT * FROM Users Where id = ?;
        return self.session.query(UsersSQLDBModel).filter(UsersSQLDBModel.id == user_id).one_or_none()        
        # django: UsersSQLDBModel.objects.filter(UsersSQLDBModel.id = user_id) ceva de genu, nu`s sigur


















    @check_session()
    def create_user(self, user_model: UsersSQLDBModel):
        self.session.add(user_model)  # nu mai rulam query-uri sql, ci ne folosim de ORM dat de sqlalchemy
        return user_model.id

    @check_session()
    def get_user_by_id(self, user_id):
        return self.session.query(UsersSQLDBModel).filter(UsersSQLDBModel.id == user_id).one_or_none()

    @check_session()
    def get_user_by_email(self, email):
        return self.session.query(UsersSQLDBModel).filter(UsersSQLDBModel.email == email).one_or_none()

    @check_session()
    def delete_user_by_id(self, user_id):
        deleted_rows = self.session.query(UsersSQLDBModel).filter(UsersSQLDBModel.id == user_id).delete()
        return deleted_rows

    @check_session()
    def update_user_by_id(self, user_id, user_data):
        # self.session.query(UsersSQLDBModel).get(user_id).update(user_data)
        affected_rows = self.session.query(UsersSQLDBModel).filter(UsersSQLDBModel.id == user_id).update(user_data)
        return affected_rows

    def __exit__(self, exc_type, exc_value, traceback):  # __exit__ e chemat in momentul can se iese din with
        if exc_type:
            self.session.rollback()
            self.session.close()
            return False
        else:
            try:
                self.session.commit()
            except Exception as err:
                logger.error(f"Commit failed: {err}")
                self.session.rollback()
                self.session.close()
        self.session.close()
