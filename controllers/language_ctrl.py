from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.language import Language
from controllers.error_ctrl import ErrorCtrl

class LanguageCtrl:
    @staticmethod
    def render_template(db: Collection):
        languages_received = db.find()
        return render_template('DB_Language.html', languages=languages_received)

    @staticmethod
    def add_language(db: Collection):
        id_language = get_next_sequence_value(db, "id_language")
        name = request.form['name']
        if id_language and name:
            language = Language(id_language, name)
            db.insert_one(language.toDBCollection())
            return redirect(url_for('languages'))
        else:
            ErrorCtrl.error_404('Language')

    @staticmethod
    def put_language(db: Collection, id_language: int):
        name = request.form.get('name')
        if id_language and name:
            id_language = int(id_language)
            matching_language = {'id_language': id_language}
            change = {'$set': {'name': name}}
            result = db.update_one(matching_language, change)
            if result.matched_count == 0:
                return ErrorCtrl.error_404('Language')
            elif result.modified_count == 0:
                return jsonify({'message': 'New language matches with actual language', 'status': '200 OK'}), 200
            return redirect(url_for('languages'))
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def put_language_param(db: Collection):
        id_language = int(request.args.get('id_language'))
        return LanguageCtrl.put_language(db, id_language)

    @staticmethod
    def put_language_form(db: Collection):
        id_language = int(request.form.get('id_language'))
        return LanguageCtrl.put_language(db, id_language)

    @staticmethod
    def delete_language(db: Collection, id_language: int):
        if id_language:
            id_language = int(id_language)
            result = db.delete_one({'id_language': id_language})
            if result.deleted_count == 1:
                return redirect(url_for('languages'))
            else:
                ErrorCtrl.error_404('Language')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def delete_language_param(db: Collection, id_language):
        return LanguageCtrl.delete_language(db, id_language)

    @staticmethod
    def delete_language_form(db: Collection):
        id_language = int(request.form.get("id_language"))
        return LanguageCtrl.delete_language(db, id_language)

    @staticmethod
    def get_all_languages(db: Collection):
        all_languages = db.find()
        language_list = [
            {
                'id_language': language.get('id_language'),
                'name': language.get('name')
            }
            for language in all_languages
        ]
        return jsonify(language_list), 200

    @staticmethod
    def get_language_by_id(db: Collection, id_language):
        if id_language:
            id_language = int(id_language)
            matching_language = db.find({'id_language': id_language})
            if matching_language:
                language_found = [
                    {
                        'id_language': language.get('id_language'),
                        'name': language.get('name')
                    }
                    for language in matching_language
                ]
                return jsonify(language_found), 200
            else:
                ErrorCtrl.error_404('Language')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def get_language_by_name(db: Collection):
        name = request.args.get('name')
        if name:
            matching_language = db.find({'name': name})
            if matching_language:
                language_found = [
                    {
                        'id_language': language.get('id_language'),
                        'name': language.get('name')
                    }
                    for language in matching_language
                ]
                return jsonify(language_found), 200
            else:
                ErrorCtrl.error_404('Language')
        else:
            ErrorCtrl.error_400()
