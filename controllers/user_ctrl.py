from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.user import User
from controllers.error_ctrl import ErrorCtrl


class UserCtrl:
    @staticmethod
    def render_template(db: Collection):
        users_received = db.find()
        return render_template('DB_User.html', users=users_received)

    @staticmethod
    def add_user(db: Collection):
        id_user = get_next_sequence_value(db, "id_user")
        username = request.form['username']
        email = request.form['email']

        if id_user:
            id_user = int(id_user)
            # user = UserClient.getUser(idUser)
            # user = User(idUser, user.get('username'), user.get('email'))
            user = User(id_user, username, email)

            db.insert_one(user.toDBCollection())
            return redirect(url_for('users'))
        else:
            ErrorCtrl.error_404('User')

    @staticmethod
    def delete_user(db: Collection, id_user: int):
        if id_user:
            id_user = int(id_user)
            result = db.delete_one({'id_user': id_user})
            if result.deleted_count == 1:
                return redirect(url_for('users'))
            else:
                ErrorCtrl.error_404('Error')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def delete_user_param(db: Collection):
        id_user = int(request.args.get('id_user'))
        return UserCtrl.delete_user(db, id_user)

    @staticmethod
    def delete_user_form(db: Collection):
        id_user = int(request.form.get('id_user'))
        return UserCtrl.delete_user(db, id_user)
