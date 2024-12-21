from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.profileUser import ProfileUser
from controllers.error_ctrl import ErrorCtrl

class ProfileCtrl:
    @staticmethod
    def render_template(db: Collection):
        profiles_received = db.find()
        return render_template('DB_ProfileUser.html', profiles=profiles_received)

    @staticmethod
    def add_profile(db: Collection):
        id_profile = get_next_sequence_value(db, "id_profile")
        name = request.form.get('name')
        id_user = request.form.get('id_user')
        id_language = request.form.get('id_language')

        if id_profile:
            id_profile = int(id_profile)
            profile_user = ProfileUser(id_profile, str(name), int(id_user), int(id_language))
            db.insert_one(profile_user.toDBCollection())
            return redirect(url_for('profiles'))
        else:
            ErrorCtrl.error_404('Profile')

    @staticmethod
    def delete_profile(db: Collection, id_profile: int):
        if id_profile:
            id_profile = int(id_profile)
            result = db.delete_one({'id_profile': id_profile})
            if result.deleted_count == 1:
                return redirect(url_for('profiles'))
            else:
                ErrorCtrl.error_404('Profile')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def delete_profile_param(db: Collection):
        id_profile = int(request.args.get('id_profile'))
        return ProfileCtrl.delete_profile(db, id_profile)

    @staticmethod
    def delete_profile_form(db: Collection):
        id_profile = int(request.form.get('id_profile'))
        return ProfileCtrl.delete_profile(db, id_profile)
