from flask import Flask, render_template
#from flask_cors import CORS

import database as dbase
from controllers.language_ctrl import LanguageCtrl
from controllers.profile_ctrl import ProfileCtrl
from controllers.review_ctrl import ReviewCtrl
from controllers.user_ctrl import UserCtrl
from controllers.view_ctrl import ViewsCtrl

db = dbase.conexionMongoDB()

app = Flask(__name__)

# CORS(app)
#CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # CORS restringido al origen React


# -------------------------------------------------------------------------------------------------------


@app.route('/')
def home():
    return render_template('index.html')


# -------------------------------------------------------------------------------------------------------


@app.route('/languages')
def languages():
    return LanguageCtrl.render_template(db['languages'])


@app.route('/languages', methods=['POST'])
def add_language():
    return LanguageCtrl.add_language(db['languages'])


@app.route('/languages', methods=['PUT'])
def put_language_form():
    return LanguageCtrl.put_language_form(db['languages'])


@app.route('/languages', methods=['DELETE'])
def delete_language_form():
    return LanguageCtrl.delete_language_form(db['languages'])


@app.route('/languages/<id_language>', methods=['PUT'])
def put_language(id_language):
    return LanguageCtrl.put_language(db['languages'], id_language)


@app.route('/languages/<id_language>', methods=['DELETE'])
def delete_language(id_language):
    return LanguageCtrl.delete_language(db['languages'], id_language)


@app.route('/languages/all')
def get_all_languages():
    return LanguageCtrl.get_all_languages(db['languages'])


@app.route('/languages/<id_language>', methods=['GET'])
def get_language_by_id(id_language):
    return LanguageCtrl.get_language_by_id(db['languages'], id_language)


@app.route('/languages', methods=['GET'])
def get_language_by_name():
    return LanguageCtrl.get_language_by_name(db['languages'])


# -------------------------------------------------------------------------------------------------------


@app.route('/reviews')
def reviews():
    return ReviewCtrl.render_template(db['reviews'])


@app.route('/reviews', methods=['POST'])
def add_review():
    return ReviewCtrl.add_review(db['reviews'])


@app.route('/reviews', methods=['PUT'])
def put_review_form():
    return ReviewCtrl.put_review_form(db['reviews'])


@app.route('/reviews', methods=['DELETE'])
def delete_review_form():
    return ReviewCtrl.delete_review_form(db['reviews'])


@app.route('/reviews/<id_review>', methods=['PUT'])
def put_review(id_review):
    return ReviewCtrl.put_review(db['reviews'], id_review)


@app.route('/reviews/<id_review>', methods=['DELETE'])
def delete_review(id_review):
    return ReviewCtrl.delete_review(db['reviews'], id_review)


@app.route('/reviews/all', methods=['GET'])
def get_all_reviews():
    return ReviewCtrl.get_all_reviews(db['reviews'])


@app.route('/reviews/<id_review>', methods=['GET'])
def get_review_by_id(id_review):
    return ReviewCtrl.get_review_by_id(db['reviews'], id_review)


@app.route('/reviews/contents', methods=['GET'])
def get_reviews_by_id_content():
    return ReviewCtrl.get_reviews_by_id_content(db['reviews'])


@app.route('/reviews/profiles', methods=['GET'])
def get_reviews_by_id_profile():
    return ReviewCtrl.get_reviews_by_id_profile(db['reviews'])


@app.route('/reviews/ratings', methods=['GET'])
def get_reviews_by_rating():
    return ReviewCtrl.get_reviews_by_rating(db['reviews'])


# TODO
@app.route('/reviews/minrating', methods=['GET'])
def get_reviews_by_min_rating():
    return ReviewCtrl.get_reviews_by_min_rating(db['reviews'])


@app.route('/reviews/maxrating', methods=['GET'])
def get_reviews_by_max_rating():
    return ReviewCtrl.get_reviews_by_max_rating(db['reviews'])


@app.route('/reviews/comments', methods=['GET'])
def get_reviews_with_commentary():
    return ReviewCtrl.get_reviews_with_commentary(db['reviews'])


@app.route('/reviews/nocomments', methods=['GET'])
def get_reviews_without_commentary():
    return ReviewCtrl.get_reviews_without_commentary(db['reviews'])


@app.route('/reviews/stats', methods=['GET'])
def get_stats_review():
    return ReviewCtrl.get_stats_review(db['reviews'])


# -------------------------------------------------------------------------------------------------------
@app.route('/profiles')
def profiles():
    return ProfileCtrl.render_template(db['profiles'])


@app.route('/profiles', methods=['POST'])
def add_profile():
    return ProfileCtrl.add_profile(db['profiles'])


@app.route('/profiles/<id_profile>', methods=['DELETE'])
def delete_profile(id_profile):
    return ProfileCtrl.delete_profile(db['profiles'], id_profile)


@app.route('/profiles', methods=['DELETE'])
def delete_profile_form():
    return ProfileCtrl.delete_profile_form(db['profiles'])


# -------------------------------------------------------------------------------------------------------
@app.route('/users')
def users():
    return UserCtrl.render_template(db['users'])


@app.route('/users', methods=['POST'])
def add_user():
    return UserCtrl.add_user(db['users'])


@app.route('/users/<id_user>', methods=['DELETE'])
def delete_user(id_profile):
    return UserCtrl.delete_user(db['users'], id_profile)


@app.route('/users', methods=['DELETE'])
def delete_user_form():
    return UserCtrl.delete_user_form(db['users'])


# -------------------------------------------------------------------------------------------------------


@app.route('/views')
def views():
    return ViewsCtrl.render_template(db['views'])


@app.route('/views', methods=['POST'])
def add_view():
    return ViewsCtrl.add_view(db['views'])


@app.route('/views', methods=['PUT'])
def put_view_form():
    return ViewsCtrl.put_view_form(db['views'])


@app.route('/views', methods=['DELETE'])
def delete_view_form():
    return ViewsCtrl.delete_view_form(db['views'])


@app.route('/views/<id_view>', methods=['PUT'])
def put_view(id_view):
    return ViewsCtrl.put_view(db['views'], id_view)


@app.route('/views/<id_view>', methods=['DELETE'])
def delete_view(id_view):
    return ViewsCtrl.delete_view(db['views'], id_view)


@app.route('/views/all', methods=['GET'])
def get_all_views():
    return ViewsCtrl.get_all_views(db['views'])


@app.route('/views/<id_view>', methods=['GET'])
def get_view_by_id(id_view):
    return ViewsCtrl.get_view_by_id(db['views'], id_view)


@app.route('/views/contents', methods=['GET'])
def get_views_by_id_content():
    return ViewsCtrl.get_views_by_id_content(db['views'])


@app.route('/views/profiles', methods=['GET'])
def get_views_by_id_profile():
    return ViewsCtrl.get_views_by_id_profile(db['views'])


@app.route('/views/stats', methods=['GET'])
def get_stats_view():
    return ViewsCtrl.get_stats_view(db['views'])


# -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8083)
