from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection
from models.language import Language

class LanguageCtrl:
    @staticmethod
    def render_template(db: Collection):
        languagesReceived = db.find()
        return render_template('DB_Language.html', languages=languagesReceived)

    @staticmethod
    def addLanguage(db: Collection):
        name = request.form['name']
        if name:
            language = Language(name)
            db.insert_one(language.toDBCollection())
            return redirect(url_for('languages'))
        else:
            return jsonify({'error': 'Language not found or not updated'}), 404

    @staticmethod
    def putLanguage(db: Collection):
        languages = db['Languages']
        actualName = request.form['actualName']
        name = request.form['name']

        if name and actualName:
            filter = {'Name': actualName}
            change = {'$set': {'Name': name}}
            result = languages.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Language not found or not updated'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'Ya tiene ese nombre', 'status': '200 OK'}), 200
            return redirect(url_for('languages'))
        else:
            return jsonify({'message': 'Faltan datos', 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteLanguage(db: Collection):
        language_name = request.form['name']
        db.delete_one({'name': language_name})
        if request.form.get('_method') == 'DELETE':
            language_name = request.form['name']
            result = db.delete_one({'name': language_name})
            if result.deleted_count == 1:
                print("Delete ok")
                return redirect(url_for('languages'))
            else:
                print("Delete failed")
                return redirect(url_for('languages'))
        else:
            return redirect(url_for('languages'))