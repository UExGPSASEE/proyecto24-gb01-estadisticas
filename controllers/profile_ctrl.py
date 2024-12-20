from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.profileUser import ProfileUser


class ProfileCtrl:
    @staticmethod
    def render_template(db: Collection):
        profilesReceived = db.find()
        return render_template('DB_ProfileUser.html', profiles=profilesReceived)

    @staticmethod
    def addProfile(db: Collection):
        idProfile = get_next_sequence_value(db, "idProfile")
        name = request.form.get('name')
        idUser = request.form.get('idUser')
        idLanguage = request.form.get('idLanguage')

        if idProfile:
            idProfile = int(idProfile)
            profileUser = ProfileUser(idProfile, str(name), int(idUser), int(idLanguage))
            db.insert_one(profileUser.toDBCollection())
            return redirect(url_for('profiles'))
        else:
            return jsonify({'error': 'Profile User not found or not added', 'status': '404 Not Found'}), 404

    @staticmethod
    def deleteProfile(db: Collection, idProfile: int):
        if idProfile:
            idProfile = int(idProfile)
            result = db.delete_one({'idProfile': idProfile})
            if result.deleted_count == 1:
                return redirect(url_for('profiles'))
            else:
                return jsonify({'error': 'Profile not found or not deleted', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteProfileParam(db: Collection):
        idProfile = int(request.args.get('idProfile'))
        return ProfileCtrl.deleteProfile(db, idProfile)

    @staticmethod
    def deleteProfileForm(db: Collection):
        idProfile = int(request.form.get('idProfile'))
        return ProfileCtrl.deleteProfile(db, idProfile)
