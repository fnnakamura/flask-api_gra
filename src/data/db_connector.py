import atexit
import csv
from math import prod
from this import d
import time
import jaydebeapi
from models.movies import MovieSchema


def singleton(cls):
    instances = {}

    def instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return instance


@singleton
class dbConnector():
    connection = None

    # "jdbc:h2:tcp://localhost:5234/movies",
    # "jdbc:h2:mem:.",
    def __init__(self):
        print("db:init")
        self.connection = jaydebeapi.connect(
            "org.h2.Driver",
            "jdbc:h2:mem:.",
            ["SA", ""],
            "./infra/h2-2.1.212.jar")
        atexit.register(self.__del__)

    def __del__(self):
        print("db:del")
        if self.connection:
            self.connection.close()

    def _execute(self, query, returnResult=False, getColumnNames=False):
        data = None
        cursor = self.connection.cursor()
        cursor.execute(query)

        if returnResult:
            data = cursor.fetchall()

        if getColumnNames:
            data = [tuple(record[0].lower()
                          for record in cursor.description)] + data

        cursor.close()

        return data

    def initialize(self, csv_filename):
        print("db:initialize")
        self._execute(
            ("CREATE TABLE IF NOT EXISTS movies ("
             "   id INTEGER PRIMARY KEY AUTO_INCREMENT,"
             "   release_year INTEGER NOT NULL,"
             "   title VARCHAR NOT NULL,"
             "   studios VARCHAR NOT NULL,"
             "   producers VARCHAR NOT NULL,"
             "   winner BOOLEAN,"
             "   created_date DATETIME NOT NULL,"
             "   modified_date DATETIME)"))
        # self._execute(
        #     ("CREATE TABLE IF NOT EXISTS MovieList("  # id INT PRIMARY KEY AUTO_INCREMENT,"
        #      "   release_year INTEGER NOT NULL,"
        #      "   title VARCHAR NOT NULL,"
        #      "   studios VARCHAR NOT NULL,"
        #      "   producers VARCHAR NOT NULL,"
        #      "   winner BOOLEAN)"
        #      " AS SELECT * FROM CSVREAD('./movielist.csv', null, 'fieldSeparator=;')"))
        # self._execute(
        #     ("ALTER TABLE MovieList ADD id INTEGER PRIMARY KEY AUTO_INCREMENT"))
        with open(csv_filename, newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                row['title'] = row['title'].replace("'", "''")
                row['studios'] = row['studios'].replace("'", "''")
                row['producers'] = row['producers'].replace("'", "''")
                if row['winner'] == 'yes':
                    row['winner'] = True
                else:
                    row['winner'] = False
                self._execute(
                    "INSERT INTO movies VALUES (DEFAULT, {year}, \'{title}\', \'{studios}\', \'{producers}\', {winner}, CURRENT_TIMESTAMP, NULL)".format(**row))

    def _get_all(self):
        data = self._execute("SELECT * FROM movies",
                             returnResult=True, getColumnNames=True)
        data[0] = tuple('year' if column ==
                        'release_year' else column for column in data[0])
        data = [dict(zip(data[0], row)) for row in data[1:]]
        # data = MovieSchema().load(column_and_values, many=True)
        # return self._execute("SELECT * FROM movies", returnResult=True)
        return data

    def _get_all_producers(self):
        data = self._execute("SELECT * FROM movies WHERE winner=True",
                             returnResult=True, getColumnNames=True)
        data[0] = tuple('year' if column ==
                        'release_year' else column for column in data[0])
        data = [dict(zip(data[0], row)) for row in data[1:]]
        producers_list = {}
        for movie in data:
            producers = [name.strip()
                         for name in movie['producers'].replace(' and ', ',').split(',') if name]
            for producer in producers:
                if producer in producers_list.keys():
                    producers_list[producer].append(movie["year"])
                else:
                    producers_list[producer] = [movie["year"]]
        return producers_list

    def get_award_intervals(self):
        producers_list = self._get_all_producers()
        # producers_list['NakamuraMax'] = [1, 9, 10, 11, 10000]
        # producers_list['NakamuraMin'] = [1, 9, 10, 11, 10000]
        award_list = {}
        fastest_winners = []
        longest_winners = []
        return_data = {'min': [], 'max': []}
        for producer in producers_list.keys():
            if len(producers_list[producer]) > 1:
                award_list[producer] = sorted(producers_list[producer])

        for producer in award_list.keys():
            interval = max(award_list[producer]) - min(award_list[producer])
            if len(longest_winners) and interval > longest_winners[0]['interval']:
                longest_winners.clear()
                longest_winners.append({
                    'producer': producer,
                    'interval': interval,
                    'previousWin': min(award_list[producer]),
                    'followingWin': max(award_list[producer])
                })
            elif len(longest_winners) and interval == longest_winners[0]['interval']:
                longest_winners.append({
                    'producer': producer,
                    'interval': interval,
                    'previousWin': min(award_list[producer]),
                    'followingWin': max(award_list[producer])
                })
            elif len(longest_winners) == 0:
                longest_winners.append({
                    'producer': producer,
                    'interval': interval,
                    'previousWin': min(award_list[producer]),
                    'followingWin': max(award_list[producer])
                })

        for producer in award_list.keys():
            min_interval = max(
                [i for sublist in award_list.values() for i in sublist])
            for pos, year in enumerate(award_list[producer][:-1]):
                interval = award_list[producer][pos+1] - year
                if interval <= min_interval:
                    min_interval = interval
                    previousWin = year
                    followingWin = award_list[producer][pos+1]
                if len(fastest_winners) and min_interval < fastest_winners[0]['interval']:
                    fastest_winners.clear()
                    fastest_winners.append({
                        'producer': producer,
                        'interval': min_interval,
                        'previousWin': previousWin,
                        'followingWin': followingWin
                    })
                elif len(fastest_winners) and interval == fastest_winners[0]['interval']:
                    fastest_winners.append({
                        'producer': producer,
                        'interval': min_interval,
                        'previousWin': previousWin,
                        'followingWin': followingWin
                    })
                elif len(fastest_winners) == 0:
                    fastest_winners.append({
                        'producer': producer,
                        'interval': min_interval,
                        'previousWin': previousWin,
                        'followingWin': followingWin
                    })

        return_data['max'] = longest_winners
        return_data['min'] = fastest_winners
        return return_data

    def get_producers(self, id=None):
        if id is None:
            return self._get_all_producers()

        # data = self._execute("SELECT * FROM movies WHERE id = {}".format(id),
        #                      returnResult=True, getColumnNames=True)
        # data[0] = tuple('year' if column ==
        #                 'release_year' else column for column in data[0])
        # data = [dict(zip(data[0], row)) for row in data[1:]]
        # return data

    def get(self, id=None):
        if id is None:
            return self._get_all()

        data = self._execute("SELECT * FROM movies WHERE id = {}".format(id),
                             returnResult=True, getColumnNames=True)
        data[0] = tuple('year' if column ==
                        'release_year' else column for column in data[0])
        data = [dict(zip(data[0], row)) for row in data[1:]]

        return data
        # if not movie:
        #    abort(404, errors={"errors": {
        #          "message": "Movie with id {} does not exist".format(Id)}})
        # return movie

    def create(self, movie):
        movie['title'] = movie['title'].replace("'", "''")
        movie['studios'] = movie['studios'].replace("'", "''")
        movie['producers'] = movie['producers'].replace("'", "''")

        count = self._execute("SELECT count(*) AS count FROM movies WHERE title LIKE '{}'".format(
            movie.get("title")), returnResult=True)

        if count[0][0] > 0:
            return False

        self._execute(
            "INSERT INTO movies VALUES(DEFAULT, {year}, \'{title}\', \'{studios}\', \'{producers}\', {winner}, CURRENT_TIMESTAMP, NULL)".format(**movie))

        return True

    # def update(exoplanet, Id):
    #     count = _execute(
    #         "SELECT count(*) AS count FROM MovieList WHERE id = {}".format(Id), returnResult=True)
    #     if count[0]["count"] == 0:
    #         return

    #     values = ["'{}'".format(value) for value in exoplanet.values()]
    #     update_values = ", ".join("{} = {}".format(key, value)
    #                               for key, value in zip(exoplanet.keys(), values))
    #     _execute("UPDATE MovieList SET {} WHERE id = {}".format(update_values, Id))

    #     return {}

    # def delete(Id):
    #     count = _execute(
    #         "SELECT count(*) AS count FROM MovieList WHERE id = {}".format(Id), returnResult=True)
    #     if count[0]["count"] == 0:
    #         return

    #     _execute("DELETE FROM MovieList WHERE id = {}".format(Id))
    #     return {}
