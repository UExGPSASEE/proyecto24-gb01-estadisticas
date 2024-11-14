import database as dbase
from flask import Flask, render_template, request, jsonify, redirect, url_for
from controllers.language_ctrl import LanguageCtrl
from controllers.review_ctrl import ReviewCtrl
from controllers.profile_ctrl import ProfileCtrl
from controllers.user_ctrl import UserCtrl
#from controllers.view_ctrl import ViewsCtrl

db = dbase.conexionMongoDB()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/languages')
def languages():
    languages = db['languages']
    languagesReceived = languages.find()
    return render_template('DB_Language.html', languages=languagesReceived)

@app.route('/languages/languageAdded', methods=['POST'])
def addLanguage():
    return LanguageCtrl.addLanguage(db['languages'])

@app.route('/languages/languageUpdated', methods=['POST'])
def putLanguage():
    return LanguageCtrl.putLanguage(db['languages'])

@app.route('/languages/languageDeleted', methods=['POST'])
def deleteLanguage():
    return LanguageCtrl.deleteLanguage(db['languages'])

@app.route('/reviews')
def reviews():
    reviews = db['reviews']
    reviewsReceived = reviews.find()
    return render_template('DB_Review.html', reviews=reviewsReceived)

@app.route('/reviews/reviewAdded', methods=['POST'])
def addReview():
    return ReviewCtrl.addReview(db['reviews'])

@app.route('/reviews/reviewUpdated', methods=['POST'])
def putReview():
    return ReviewCtrl.putReview(db['reviews'])

@app.route('/reviews/reviewDeleted', methods=['POST'])
def deleteReview():
    return ReviewCtrl.deleteReview(db['reviews'])

@app.route('/reviews/reviewFound', methods=['GET'])
def getReviewById():
    return ReviewCtrl.getReviewById(db['reviews'])

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

@app.route('/users')
def users():
    users = db['users']
    usersReceived = users.find()
    return render_template('DB_User.html', users=usersReceived)

@app.route('/users/userAdded', methods=['POST'])
def addUser():
    return UserCtrl.addUser(db['users'])

@app.route('/users/userUpdated', methods=['POST'])
def putUser():
    return UserCtrl.putUser(db['users'])

@app.route('/users/userDeleted', methods=['POST'])
def deleteUser():
    return UserCtrl.deleteUser(db['users'])

if __name__ == '__main__':
    app.run(debug=True, port=8083)