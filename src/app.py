import json
import os
import sys
from api.awards_api import AwardsApi
from flask import Flask
from flask_restful import Api

from routes import movie_bp
from data.db_connector import dbConnector
from api.movies_api import MoviesApi
from api.producers_api import ProducersApi

app = Flask(__name__, template_folder='templates')
api = Api(app)

app.register_blueprint(movie_bp, url_prefix='/')
api.add_resource(MoviesApi, "/api/movies", "/api/movies/<int:id>")
api.add_resource(ProducersApi, "/api/producers", "/api/producers/<int:id>")
api.add_resource(AwardsApi, "/api/awards")

if __name__ == "__main__":
    curr_dir = os.getcwd()
    param_full_path = curr_dir+'/'+sys.argv[1]
    print(param_full_path)

    db = dbConnector()
    db.initialize(param_full_path)

    app.run(debug=True)
