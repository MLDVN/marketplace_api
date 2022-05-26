from sqlalchemy import Column, String

from database.sql import Base
from database.sqlalchemy_serializer import SQLAlchemySerializer

# "b4da16a1-b23f-42c8-aff0-371539fe1553": {
#             "name": "John Doe",
#             "email": "john_doe@gmail.com",
#             "register_date": "2022-04-13 20:44"
#         },


class UsersSQLDBModel(Base, SQLAlchemySerializer):
    __tablename__ = f'Users'

    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    register_date = Column(String)

    def __init__(self, **fields):
        self.id = fields.get('user_id', None)
        self.name = fields.get('name')
        self.email = fields.get('email')
        self.register_date = fields.get('register_date')

    def __repr__(self):  # functie folosita daca vrem sa printam o instanta de model
        return f"<User> name:{self.name}; email:{self.email}; register_date: {self.register_date}"
