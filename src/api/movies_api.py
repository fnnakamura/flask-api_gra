import json
from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from data.db_connector import dbConnector
from models.movies import MovieSchema


class MoviesApi(Resource):
    db = dbConnector()

    def get(self, id=None):
        if id is None:
            return self.db.get()

        return self.db.get(id)

    def post(self):
        try:
            print(request.json)
            # movie = MovieSchema(
            #     exclude=['id', 'created_date', 'modified_date']).load(json.dumps(request.json))
            if not self.db.create(request.json):
                abort(404, errors={"errors": {
                      "message": "Movie with title {} already exists".format(request.json["title"])}})
        except ValidationError as e:
            abort(405, errors=e.messages)

        # def put(self, Id):
        #     try:
        #         exoplanet = db_connector.ExoplanetSchema(
        #             exclude=["id"]).loads(request.json)
        #         if not db_connector.update(exoplanet, Id):
        #             abort(404, errors={"errors": {
        #                   "message": "Exoplanet with Id {} does not exist".format(Id)}})
        #     except ValidationError as e:
        #         abort(405, errors=e.messages)

        # def delete(self, Id):
        #     if not db_connector.delete(Id):
        #         abort(404, errors={"errors": {
        #               "message": "Exoplanet with Id {} does not exist".format(Id)}})
