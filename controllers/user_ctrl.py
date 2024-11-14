from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection
from models.user import User

class UserCtrl:
    @staticmethod
    def render_template(db: Collection):
        usersReceived = db.find()
        return render_template('DB_User.html', users=usersReceived)

    @staticmethod        
    def get_next_sequence_value(db: Collection, sequence_name):        
        counter = db.find_one({"_id": sequence_name})

        if counter is None:       
            db.insert_one({"_id": sequence_name, "sequence_value": 1})
            return 1
        
        updated_counter = db.find_one_and_update(
            {"_id": sequence_name},
            {"$inc": {"sequence_value": 1}},
            return_document=True
        )
        return updated_counter["sequence_value"]

    @staticmethod
    def addUser(db: Collection):
        idUser = UserCtrl.get_next_sequence_value(db,"idUser")
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if idUser:
            user = User(idUser, username, email, password)
            db.insert_one(user.toDBCollection())
            return redirect(url_for('users'))
        else:
            return jsonify({'error': 'User not found or not added', 'status':'404 Not Found'}), 404

    @staticmethod
    def putUser(db: Collection):
        idUser = int(request.form.get('idUser'))
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if idUser and (request.form.get('method') == 'PUT'):
            filter = {'idUser': idUser}
            change = {'$set': {'username': username, 'email': email, 'password':password}}
            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'User not found or not updated', 'status':'404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'New user matches with actual user', 'status': '200 OK'}), 200
            return redirect(url_for('users'))
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteUser(db: Collection):
        idUser = int(request.form.get('idUser'))
        if request.form.get('method') == 'DELETE' and idUser:
            result = db.delete_one({'idUser': idUser})
            if result.deleted_count == 1:
                return redirect(url_for('users'))
            else:
                return jsonify({'error': 'User not found or not deleted', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400