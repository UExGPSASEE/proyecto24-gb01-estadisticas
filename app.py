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
    languages = db['Languages']
    languagesReceived = languages.find()
    return render_template('DB_Language.html', languages=languagesReceived)

@app.route('/languages/addLanguage', methods=['POST'])
def addLanguage():
    languages = db['Languages']
    name = request.form['name']

    if name:
        language = Language(name)
        languages.insert_one(language.toDBCollection())
        return redirect(url_for('languages'))
    else:
        return notFound()

@app.route('/languages/putLanguage', methods=['POST'])
def putLanguage():
    languages = db['Languages']
    actualName = request.form['actualName']
    name = request.form['name']

    if name and actualName:
        filter = {'Name':actualName}
        change = {'$set':{'Name':name}}
        result = languages.update_one(filter, change)
        if result.matched_count == 0:
            return notFound()
        elif result.modified_count == 0:
            return jsonify({'message' : 'Ya tiene ese nombre','status' : '200 OK'}),200
        return redirect(url_for('languages'))
    else:
        return jsonify({'message' : 'Faltan datos','status' : '400 Bad Request'}),400

@app.route('/languages/delete/<string:languages_name>', methods=['DELETE'])
def deleteLanguage(language_name):
    languages = db['Languages']
    languages.delete_one({'name' : language_name})
    return redirect(url_for('home'))

@app.route('/reviews')
def reviews():
    reviews = db['Reviews']
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
        return redirect(url_for('reviews'))
    else:
        return notFound()
    
@app.route('/reviews/putReview', methods=['POST'])
def putReview():
    reviews = db['Reviews']
    actualProfile = request.form['Profile']
    actualContent_id = request.form['Content_id']
    valoracion = request.form['Valoracion']
    comentario = request.form['Comentario']

    if actualProfile and actualContent_id and valoracion:
        filter = {'Profile':actualProfile,'Content_id':actualContent_id}
        if comentario:
            change = {'$set':{'Profile':actualProfile,'Content_id':actualContent_id,'Valoracion':valoracion,'Comentario':comentario}}
        else:
            change = {'$set':{'Profile':actualProfile,'Content_id':actualContent_id,'Valoracion':valoracion}}
        result = reviews.update_one(filter, change)
        if result.matched_count == 0:
            return notFound()
        elif result.modified_count == 0:
            return jsonify({'message' : 'Ya tiene esa valoracion y/o comentario','status' : '200 OK'}),200
        return redirect(url_for('reviews'))
    else:
        return jsonify({'message' : 'Faltan datos','status' : '400 Bad Request'}),400

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