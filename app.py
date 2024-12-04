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
def addLanguage():
    return LanguageCtrl.addLanguage(db['languages'])


@app.route('/languages', methods=['PUT'])
def putLanguageForm():
    return LanguageCtrl.putLanguageForm(db['languages'])


@app.route('/languages', methods=['DELETE'])
def deleteLanguageForm():
    return LanguageCtrl.deleteLanguageForm(db['languages'])


@app.route('/languages/<idLanguage>', methods=['PUT'])
def putLanguage(idLanguage):
    return LanguageCtrl.putLanguage(db['languages'], idLanguage)


@app.route('/languages/<idLanguage>', methods=['DELETE'])
def deleteLanguage(idLanguage):
    return LanguageCtrl.deleteLanguage(db['languages'], idLanguage)


@app.route('/languages/all')
def getAllLanguages():
    return LanguageCtrl.getAllLanguages(db['languages'])


@app.route('/languages/<idLanguage>', methods=['GET'])
def getLanguageById(idLanguage):
    return LanguageCtrl.getLanguageById(db['languages'], idLanguage)


@app.route('/languages', methods=['GET'])
def getLanguageByName():
    return LanguageCtrl.getLanguageByName(db['languages'])


# -------------------------------------------------------------------------------------------------------


@app.route('/reviews')
def reviews():
    return ReviewCtrl.render_template(db['reviews'])


@app.route('/reviews', methods=['POST'])
def addReview():
    return ReviewCtrl.addReview(db['reviews'])


@app.route('/reviews', methods=['PUT'])
def putReviewForm():
    return ReviewCtrl.putReviewForm(db['reviews'])


@app.route('/reviews', methods=['DELETE'])
def deleteReviewForm():
    return ReviewCtrl.deleteReviewForm(db['reviews'])


@app.route('/reviews/<idReview>', methods=['PUT'])
def putReview(idReview):
    return ReviewCtrl.putReview(db['reviews'], idReview)


@app.route('/reviews/<idReview>', methods=['DELETE'])
def deleteReview(idReview):
    return ReviewCtrl.deleteReview(db['reviews'], idReview)


@app.route('/reviews/all', methods=['GET'])
def getAllReviews():
    return ReviewCtrl.getAllReviews(db['reviews'])


@app.route('/reviews/<idReview>', methods=['GET'])
def getReviewById(idReview):
    return ReviewCtrl.getReviewById(db['reviews'], idReview)


@app.route('/reviews/contents', methods=['GET'])
def getReviewsByIdContent():
    return ReviewCtrl.getReviewsByIdContent(db['reviews'])


@app.route('/reviews/profiles', methods=['GET'])
def getReviewsByIdProfile():
    return ReviewCtrl.getReviewsByIdProfile(db['reviews'])


@app.route('/reviews/ratings', methods=['GET'])
def getReviewsByRating():
    return ReviewCtrl.getReviewsByRating(db['reviews'])


# TODO
@app.route('/reviews/minrating', methods=['GET'])
def getReviewsByMinRating():
    return ReviewCtrl.getReviewsByMinRating(db['reviews'])


@app.route('/reviews/maxrating', methods=['GET'])
def getReviewsByMaxRating():
    return ReviewCtrl.getReviewsByMaxRating(db['reviews'])


@app.route('/reviews/comments', methods=['GET'])
def getReviewsWithCommentary():
    return ReviewCtrl.getReviewsWithCommentary(db['reviews'])


@app.route('/reviews/nocomments', methods=['GET'])
def getReviewsWithoutCommentary():
    return ReviewCtrl.getReviewsWithoutCommentary(db['reviews'])


@app.route('/reviews/stats', methods=['GET'])
def getStatsReview():
    return ReviewCtrl.getStatsReview(db['reviews'])


# -------------------------------------------------------------------------------------------------------
@app.route('/profiles')
def profiles():
    return ProfileCtrl.render_template(db['profiles'])


@app.route('/profiles', methods=['POST'])
def addProfile():
    return ProfileCtrl.addProfile(db['profiles'])


@app.route('/profiles/<idProfile>', methods=['DELETE'])
def deleteProfile(idProfile):
    return ProfileCtrl.deleteProfile(db['profiles'], idProfile)


@app.route('/profiles', methods=['DELETE'])
def deleteProfileForm():
    return ProfileCtrl.deleteProfileForm(db['profiles'])


# -------------------------------------------------------------------------------------------------------
@app.route('/users')
def users():
    return UserCtrl.render_template(db['users'])


@app.route('/users', methods=['POST'])
def addUser():
    return UserCtrl.addUser(db['users'])


@app.route('/users/<idUser>', methods=['DELETE'])
def deleteUser(idProfile):
    return UserCtrl.deleteUser(db['users'], idProfile)


@app.route('/users', methods=['DELETE'])
def deleteUserForm():
    return UserCtrl.deleteUserForm(db['users'])


# -------------------------------------------------------------------------------------------------------


@app.route('/views')
def views():
    return ViewsCtrl.render_template(db['views'])


@app.route('/views', methods=['POST'])
def addView():
    return ViewsCtrl.addView(db['views'])


@app.route('/views', methods=['PUT'])
def putViewForm():
    return ViewsCtrl.putViewForm(db['views'])


@app.route('/views', methods=['DELETE'])
def deleteViewForm():
    return ViewsCtrl.deleteViewForm(db['views'])


@app.route('/views/<idView>', methods=['PUT'])
def putView(idView):
    return ViewsCtrl.putView(db['views'], idView)


@app.route('/views/<idView>', methods=['DELETE'])
def deleteView(idView):
    return ViewsCtrl.deleteView(db['views'], idView)


@app.route('/views/all', methods=['GET'])
def getAllViews():
    return ViewsCtrl.getAllViews(db['views'])


@app.route('/views/<idView>', methods=['GET'])
def getViewById(idView):
    return ViewsCtrl.getViewById(db['views'], idView)


@app.route('/views/contents', methods=['GET'])
def getViewsByIdContent():
    return ViewsCtrl.getViewsByIdContent(db['views'])


@app.route('/views/profiles', methods=['GET'])
def getViewsByIdProfile():
    return ViewsCtrl.getViewsByIdProfile(db['views'])


@app.route('/views/stats', methods=['GET'])
def getStatsView():
    return ViewsCtrl.getStatsView(db['views'])


# -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8083)
