import json
from flask import redirect, render_template, request, url_for
from data.db_connector import dbConnector
from models.movies import MovieSchema


def index():
    db = dbConnector()
    movies_list = db.get()
    return render_template('index.html', movies_list=movies_list)


def add():
    db = dbConnector()
    if request.method == 'POST':
        movie = MovieSchema().load(request.form.to_dict())
        # movie['year'] = request.form['year']
        # movie['title'] = request.form['title']
        # movie['studios'] = request.form['studios']
        # movie['producers'] = request.form['producers']
        # movie['winner'] = request.form['winner']
        db.create(movie=movie)
        return redirect(url_for('movie_bp.index'))
    return render_template('add.html')


def edit(movie_id):
    movie = {}
    if request.method == 'POST':
        # movie.year = request.form['year']
        # movie.title = request.form['title']
        # movie.studios = request.form['studios']
        # movie.producers = request.form['producers']
        # movie.winner = request.form['winner']
        # commit ?
        return redirect(url_for('index'))
    return render_template('edit.html')


def delete(id):
    movie = {}
    # TODO: delete movie from database
    return redirect(url_for('index'))


def show(id):
    movie = {}
    # TODO: delete movie from database
    return redirect(url_for('index'))
