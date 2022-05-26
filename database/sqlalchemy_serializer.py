from sqlalchemy.inspection import inspect


class SQLAlchemySerializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(a_list_of_objects):
        return [m.serialize() for m in a_list_of_objects]