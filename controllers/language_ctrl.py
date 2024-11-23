from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.language import Language


class LanguageCtrl:
    @staticmethod
    def render_template(db: Collection):
        languagesReceived = db.find()
        return render_template('DB_Language.html', languages=languagesReceived)

    @staticmethod
    def addLanguage(db: Collection):
        idLanguage = get_next_sequence_value(db, "idLanguage")
        name = request.form['name']
        if idLanguage and name:
            language = Language(idLanguage, name)
            db.insert_one(language.toDBCollection())
            return redirect(url_for('languages'))
        else:
            return jsonify({'error': 'Language not found or not added', 'status': '404 Not Found'}), 404

    @staticmethod
    def putLanguage(db: Collection, idLanguage: int):
        name = request.form.get('name')
        if idLanguage and name:
            idLanguage = int(idLanguage)
            filter = {'idLanguage': idLanguage}
            change = {'$set': {'name': name}}
            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Language not found or not updated', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'New language matches with actual language', 'status': '200 OK'}), 200
            return redirect(url_for('languages'))
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def putLanguageParam(db: Collection):
        idLanguage = int(request.args.get('idLanguage'))
        return LanguageCtrl.putLanguage(db, idLanguage)

    @staticmethod
    def putLanguageForm(db: Collection):
        idLanguage = int(request.form.get('idLanguage'))
        return LanguageCtrl.putLanguage(db, idLanguage)

    @staticmethod
    def deleteLanguage(db: Collection, idLanguage: int):
        if idLanguage:
            idLanguage = int(idLanguage)
            result = db.delete_one({'idLanguage': idLanguage})
            if result.deleted_count == 1:
                return redirect(url_for('languages'))
            else:
                return jsonify({'error': 'Language not found or not deleted', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteLanguageParam(db: Collection, idLanguage):
        return LanguageCtrl.deleteLanguage(db, idLanguage)

    @staticmethod
    def deleteLanguageForm(db: Collection):
        idLanguage = int(request.form.get("idLanguage"))
        return LanguageCtrl.deleteLanguage(db, idLanguage)

    @staticmethod
    def getAllLanguages(db: Collection):
        allLanguages = db.find()
        language_list = [
            {
                'idLanguage': language.get('idLanguage'),
                'name': language.get('name')
            }
            for language in allLanguages
        ]
        return jsonify(language_list), 200

    @staticmethod
    def getLanguageById(db: Collection, idLanguage):
        if idLanguage:
            idLanguage = int(idLanguage)
            matching_language = db.find({'idLanguage': idLanguage})
            if matching_language:
                languageFound = [
                    {
                        'idLanguage': language.get('idLanguage'),
                        'name': language.get('name')
                    }
                    for language in matching_language
                ]
                return jsonify(languageFound), 200
            else:
                return jsonify({'error': 'Language not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getLanguageByName(db: Collection):
        name = request.args.get('name')
        if name:
            matching_language = db.find({'name': name})
            if matching_language:
                languageFound = [
                    {
                        'idLanguage': language.get('idLanguage'),
                        'name': language.get('name')
                    }
                    for language in matching_language
                ]
                return jsonify(languageFound), 200
            else:
                return jsonify({'error': 'Language not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400
