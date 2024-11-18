from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection
from models.profileUser import ProfileUser
from database import get_next_sequence_value as get_next_sequence_value

class ProfileCtrl:
    @staticmethod
    def render_template(db: Collection):
        profilesReceived = db.find()
        return render_template('DB_ProfileUser.html', profiles=profilesReceived)

    @staticmethod
    def addProfile(db: Collection):
        idProfileUser = get_next_sequence_value(db,"idProfileUser")
        name = request.form['name']
        pin = request.form['pin']
        idUser = request.form['idUser']
        idLanguage = request.form['idLanguage']

        if idProfileUser:
            profileUser = ProfileUser(idProfileUser, str(name), int(pin), int(idUser), int(idLanguage))
            db.insert_one(profileUser.toDBCollection())
            return redirect(url_for('profiles'))
        else:
            return jsonify({'error': 'Profile User not found or not added', 'status':'404 Not Found'}), 404

    @staticmethod
    def putProfile(db: Collection):
        idProfile = int(request.form.get('idProfile'))
        name = request.form.get('name')
        pin = request.form.get('pin')
        idLanguage = request.form.get('idLanguage')
        if idProfile and name and pin and (request.form.get('method') == 'PUT'):
            filter = {'idProfileUser': idProfile}
            if idLanguage:
                change = {'$set': {'name': name, 'pin': pin, 'idLanguage':idLanguage}}
            else:
                change = {'$set': {'name': name, 'pin': pin}}
            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Profile not found or not updated', 'status':'404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'New profile matches with actual profile', 'status': '200 OK'}), 200
            return redirect(url_for('profiles'))
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400


    @staticmethod
    def deleteProfile(db: Collection):
        idProfile = int(request.form.get('idProfile'))
        if request.form.get('method') == 'DELETE' and idProfile:
            result = db.delete_one({'idProfileUser': idProfile})
            if result.deleted_count == 1:
                return redirect(url_for('profiles'))
            else:
                return jsonify({'error': 'Profile not found or not deleted', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400