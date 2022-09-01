from flask_restful import Resource
from data.db_connector import dbConnector


class ProducersApi(Resource):
    db = dbConnector()

    def get(self, id=None):
        if id is None:
            return self.db.get_producers()

        # return self.db.get_producers(id)
