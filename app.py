import database as dbase
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models.language import Language
from models.review import Review

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

@app.route('/languages/addLanguage', methods=['POST'])
def addLanguage():
    languages = db['Languages']
    name = request.form['name']

    if name:
        language = Language(name)
        languages.insert_one(language.toDBCollection())
        response = jsonify({
            'name' : name
        })
        return redirect(url_for('languages'))
    else:
        return notFound()

@app.route('/languages/put/<string:languages_name>', methods=['PUT'])
def putLanguage(language_name):
    languages = db['Languages']
    name = request.form['name']

    if name:
        languages.update_one({'name' : language_name}, {'$set' : {'name' : name}})
        response = jsonify({'message' : 'Language' + language_name + 'updated.'})
        return redirect(url_for('home'))
    else:
        return notFound()

@app.route('/languages/delete/<string:languages_name>', methods=['DELETE'])
def deleteLanguage(language_name):
    languages = db['Languages']
    languages.delete_one({'name' : language_name})
    return redirect(url_for('home'))

@app.route('/reviews')
def reviews():
    reviews = db['reviews']
    reviewsReceived = reviews.find()
    return render_template('DB_Review.html', reviews=reviewsReceived)

@app.route('/reviews/addReview', methods=['POST'])
def addReview():
    reviews = db['Reviews']
    content_id = request.form['Content_id']
    valoracion = request.form['Valoracion']
    comentario = request.form['Comentario']
    profile = request.form['Profile']

    if profile:
        review = Review(content_id, valoracion, comentario, profile)
        reviews.insert_one(review.toDBCollection())
        response = jsonify({
            'content_id' : content_id,
            'valoracion' : valoracion,
            'comentario' : comentario,
            'profile' : profile
        })
        return redirect(url_for('reviews'))
    else:
        return notFound()


@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message' : 'No encontrado' + request.url,
        'status' : '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response 

if __name__ == '__main__':
    app.run(debug=True, port=8080)