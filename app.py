from flask import Flask, render_template
from flask_cors import CORS

import database as dbase
from controllers.language_ctrl import LanguageCtrl
from controllers.profile_ctrl import ProfileCtrl
from controllers.review_ctrl import ReviewCtrl
from controllers.user_ctrl import UserCtrl
from controllers.view_ctrl import ViewsCtrl

db = dbase.conexionMongoDB()

app = Flask(__name__)

# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # CORS restringido al origen React


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
def putLanguage():
    return LanguageCtrl.putLanguageParam(db['languages'])


@app.route('/languages/<idLanguage>', methods=['DELETE'])
def deleteLanguage():
    return LanguageCtrl.deleteLanguageParam(db['languages'])


# @app.route('/languages/all')
# def getAllLanguages():
#     # TODO
#     return LanguageCtrl.getAllViews(db['languages'])

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
def putReview():
    return ReviewCtrl.putReviewParam(db['reviews'])


@app.route('/reviews/<idReview>', methods=['DELETE'])
def deleteReview():
    return ReviewCtrl.deleteReviewParam(db['reviews'])


@app.route('/reviews/all', methods=['GET'])
def getAllReviews():
    return ReviewCtrl.getAllReviews(db['reviews'])


@app.route('/reviews/<idReview>', methods=['GET'])
def getReviewById():
    return ReviewCtrl.getReviewById(db['reviews'])


@app.route('/reviews/reviewsByIdContent', methods=['GET'])
def getReviewsByIdContent():
    return ReviewCtrl.getReviewsByIdContent(db['reviews'])


@app.route('/reviews/reviewsByIdProfile', methods=['GET'])
def getReviewsByIdProfile():
    return ReviewCtrl.getReviewsByIdProfile(db['reviews'])


@app.route('/reviews/reviewsByRating', methods=['GET'])
def getReviewsByRating():
    return ReviewCtrl.getReviewsByRating(db['reviews'])


@app.route('/reviews/reviewsByMinRating', methods=['GET'])
def getReviewsByMinRating():
    return ReviewCtrl.getReviewsByMinRating(db['reviews'])


@app.route('/reviews/reviewsByMaxRating', methods=['GET'])
def getReviewsByMaxRating():
    return ReviewCtrl.getReviewsByMaxRating(db['reviews'])


@app.route('/reviews/reviewsWithCommentary', methods=['GET'])
def getReviewsWithCommentary():
    return ReviewCtrl.getReviewsWithCommentary(db['reviews'])


@app.route('/reviews/reviewsWithoutCommentary', methods=['GET'])
def getReviewsWithoutCommentary():
    return ReviewCtrl.getReviewsWithoutCommentary(db['reviews'])


@app.route('/reviews/stats', methods=['GET'])
def getStatsReview():
    return ReviewCtrl.getStatsReview(db['reviews'])


# -------------------------------------------------------------------------------------------------------
@app.route('/profiles')
def profiles():
    profiles = db['profiles']
    profilesReceived = profiles.find()
    return render_template('DB_ProfileUser.html', profiles=profilesReceived)


@app.route('/profiles/profileAdded', methods=['POST'])
def addProfile():
    return ProfileCtrl.addProfile(db['profiles'])


@app.route('/profiles/profileUpdated', methods=['POST'])
def putProfile():
    return ProfileCtrl.putProfile(db['profiles'])


@app.route('/profiles/profileDeleted', methods=['POST'])
def deleteProfile():
    return ProfileCtrl.deleteProfile(db['profiles'])


# -------------------------------------------------------------------------------------------------------
@app.route('/users')
def users():
    return UserCtrl.render_template(db['users'])


@app.route('/users', methods=['POST'])
def addUser():
    return UserCtrl.addUser(db['users'])


@app.route('/users/userUpdated', methods=['POST'])
def putUser():
    return UserCtrl.putUser(db['users'])


@app.route('/users/userDeleted', methods=['POST'])
def deleteUser():
    return UserCtrl.deleteUser(db['users'])


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
def putView():
    return ViewsCtrl.putViewParam(db['views'])


@app.route('/views/<idView>', methods=['DELETE'])
def deleteView():
    return ViewsCtrl.deleteViewParam(db['views'])


@app.route('/views/all', methods=['GET'])
def getAllViews():
    return ViewsCtrl.getAllViews(db['views'])


@app.route('/views/<idView>', methods=['GET'])
def getViewById():
    return ViewsCtrl.getViewById(db['views'])


@app.route('/views/viewsByIdContent', methods=['GET'])
def getViewsByIdContent():
    return ViewsCtrl.getViewsByIdContent(db['views'])


@app.route('/views/viewsByIdProfile', methods=['GET'])
def getViewsByIdProfile():
    return ViewsCtrl.getViewsByIdProfile(db['views'])


@app.route('/views/stats', methods=['GET'])
def getStatsView():
    return ViewsCtrl.getStatsView(db['views'])


# -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8083)
