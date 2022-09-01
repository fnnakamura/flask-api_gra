from flask_restful import Resource
from data.db_connector import dbConnector


class AwardsApi(Resource):
    db = dbConnector()

    def get(self):
        return self.db.get_award_intervals()
