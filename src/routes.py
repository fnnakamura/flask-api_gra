from flask import Blueprint
from controllers.movies_controller import index, add, show, edit, delete

movie_bp = Blueprint('movie_bp', __name__)
movie_bp.route('/', methods=['GET'])(index)
movie_bp.route('/add', methods=['GET', 'POST'])(add)
movie_bp.route('/<int:movie_id>', methods=['GET'])(show)
movie_bp.route('/<int:movie_id>/edit', methods=['GET', 'POST'])(edit)
movie_bp.route('/<int:movie_id>', methods=['DELETE'])(delete)


# @app.route('/')
# @app.route('/add', methods=['GET', 'POST'])
# @app.route('/delete/<int:id>')
# @app.route('/edit/<int:id>')
