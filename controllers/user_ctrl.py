from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.user import User
from controllers.error_ctrl import ErrorCtrl


class UserCtrl:
    @staticmethod
    def render_template(db: Collection):
        usersReceived = db.find()
        return render_template('DB_User.html', users=usersReceived)

    @staticmethod
    def addUser(db: Collection):
        idUser = get_next_sequence_value(db, "idUser")
        username = request.form['username']
        email = request.form['email']

        if idUser:
            idUser = int(idUser)
            # user = UserClient.getUser(idUser)
            # user = User(idUser, user.get('username'), user.get('email'))
            user = User(idUser, username, email)

            db.insert_one(user.toDBCollection())
            return redirect(url_for('users'))
        else:
            ErrorCtrl.error_404('User')

    @staticmethod
    def deleteUser(db: Collection, idUser: int):
        if idUser:
            idUser = int(idUser)
            result = db.delete_one({'idUser': idUser})
            if result.deleted_count == 1:
                return redirect(url_for('users'))
            else:
                ErrorCtrl.error_404('Error')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def deleteUserParam(db: Collection):
        idUser = int(request.args.get('idUser'))
        return UserCtrl.deleteUser(db, idUser)

    @staticmethod
    def deleteUserForm(db: Collection):
        idUser = int(request.form.get('idUser'))
        return UserCtrl.deleteUser(db, idUser)
