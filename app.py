import database as dbase
from flask import Flask, render_template, request, jsonify, redirect, url_for
from language import Language

db = dbase.conexionMongoDB()

app = Flask(__name__)

@app.route('/')
def home():
    languages = db['Languages']
    languagesReceived = languages.find()
    return render_template('index.html', languages = languagesReceived)

@app.route('/languages', methods=['POST'])
def addLanguage():
    languages = db['Languages']
    name = request.form['name']

    if name:
        language = Language(name)
        languages.insert_one(language.toDBCollection())
        response = jsonify({
            'name' : name
        })
        return redirect(url_for('home'))
    else:
        return notFound()
    
@app.route('/languages/delete/<string:languages_name>', methods=['DELETE'])
def deleteLanguage(language_name):
    languages = db['Languages']
    languages.delete_one({'name' : language_name})
    return redirect(url_for('home'))

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