from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.views import View
from clients.contenidos_client import ContenidosClient
from models.content import ContentType
from controllers.error_ctrl import ErrorCtrl

class ViewsCtrl:
    @staticmethod
    def render_template(db: Collection):
        views_received = db.find()
        content_types = [(ct.name, ct.value) for ct in ContentType]
        return render_template('DB_Views.html', views=views_received, content_types=content_types)

    @staticmethod
    def add_view(db: Collection):
        id_view = get_next_sequence_value(db, "id_view")
        date_init = request.form.get('date_init')
        date_finish = request.form.get('date_finish')
        id_profile = request.form.get('id_profile')
        id_content = request.form.get('id_content')
        content_type = request.form.get('content_type')

        if id_view and id_content:
            if ContenidosClient.check_content_exists(int(id_content), int(content_type)):
                if not date_finish:
                    date_finish = None
                    is_finished = False
                else:
                    is_finished = True

                view = View(id_view, date_init, is_finished, date_finish, int(id_profile), int(id_content), int(content_type))
                db.insert_one(view.toDBCollection())
                return redirect(url_for('views'))

            else:
                ErrorCtrl.error_404('View')
        else:
            return jsonify({'error': 'Error when creating view', 'status': '500 Internal Server Error'}), 500

    @staticmethod
    def put_view(db: Collection, id_view: int):
        date_finish = request.form.get('date_finish')
        if id_view and date_finish:
            id_view = int(id_view)
            matching_view = {'id_view': id_view}
            change = {'$set': {'is_finished': True, 'date_finish': date_finish}}
            result = db.update_one(matching_view, change)
            if result.matched_count == 0:
                ErrorCtrl.error_404('View')
            elif result.modified_count == 0:
                return jsonify({'message': 'New view matches with actual view', 'status': '200 OK'}), 200
            return redirect(url_for('views'))
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def put_view_param(db: Collection):
        id_view = int(request.args.get('id_view'))
        return ViewsCtrl.put_view(db, id_view)

    @staticmethod
    def put_view_form(db: Collection):
        id_view = int(request.form.get('id_view'))
        return ViewsCtrl.put_view(db, id_view)

    @staticmethod
    def delete_view(db: Collection, id_view: int):
        if id_view:
            id_view = int(id_view)
            result = db.delete_one({'id_view': id_view})
            if result.deleted_count == 1:
                return redirect(url_for('views'))
            else:
                ErrorCtrl.error_404('View')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def delete_view_param(db: Collection):
        id_view = int(request.args.get('id_view'))
        return ViewsCtrl.delete_view(db, id_view)

    @staticmethod
    def delete_view_form(db: Collection):
        id_view = int(request.form.get('id_view'))
        return ViewsCtrl.delete_view(db, id_view)

    @staticmethod
    def get_all_views(db: Collection):
        all_views = db.find()
        view_list = [
            {
                'id_view': view.get('id_view'),
                'date_init': view.get('date_init'),
                'is_finished': view.get('is_finished'),
                'date_finish': view.get('date_finish'),
                'id_content': view.get('id_content'),
                'id_profile': view.get('id_profile')
            }
            for view in all_views
        ]
        if view_list.__len__()>0:
            return jsonify(view_list), 200
        else:
            ErrorCtrl.error_404('View')

    @staticmethod
    def get_view_by_id(db: Collection, id_view):
        if id_view:
            id_view = int(id_view)
            matching_view = db.find({'id_view': id_view})
            if matching_view:
                view_list = [
                    {
                        'id_view': view.get('id_view'),
                        'date_init': view.get('date_init'),
                        'is_finished': view.get('is_finished'),
                        'date_finish': view.get('date_finish'),
                        'id_content': view.get('id_content'),
                        'id_profile': view.get('id_profile')
                    }
                    for view in matching_view
                ]

                if view_list.__len__() > 0:
                    return jsonify(view_list), 200
                else:
                    ErrorCtrl.error_404('View')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def get_views_by_id_content(db: Collection):
        id_content = request.args.get('id_content')
        if id_content:
            id_content = int(id_content)
            matching_view = db.find({'id_content': id_content})
            view_list = [
                {
                    'id_view': view.get('id_view'),
                    'date_init': view.get('date_init'),
                    'is_finished': view.get('is_finished'),
                    'date_finish': view.get('date_finish'),
                    'id_content': view.get('id_content'),
                    'id_profile': view.get('id_profile')
                }
                for view in matching_view
            ]

            if view_list.__len__() > 0:
                return jsonify(view_list), 200
            else:
                ErrorCtrl.error_404('View')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def get_views_by_id_profile(db: Collection):
        id_profile = request.args.get('id_profile')
        if id_profile:
            id_profile = int(id_profile)
            matching_view = db.find({'id_profile': id_profile})
            view_list = [
                {
                    'id_view': view.get('id_view'),
                    'date_init': view.get('date_init'),
                    'is_finished': view.get('is_finished'),
                    'date_finish': view.get('date_finish'),
                    'id_content': view.get('id_content'),
                    'id_profile': view.get('id_profile')
                }
                for view in matching_view
            ]

            if view_list.__len__() > 0:
                return jsonify(view_list), 200
            else:
                ErrorCtrl.error_404('View')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def get_stats_view(db: Collection):
        id_content = request.args.get('id_content')
        if id_content:
            id_content = int(id_content)
            matching_view = db.find({'id_content': id_content})
            view_list = [
                {
                    'id_view': view.get('id_view'),
                    'date_init': view.get('date_init'),
                    'is_finished': view.get('is_finished'),
                    'date_finish': view.get('date_finish'),
                    'id_content': view.get('id_content'),
                    'id_profile': view.get('id_profile')
                }
                for view in matching_view
            ]

            if view_list.__len__() > 0:
                return jsonify(view_list), 200
            else:
                ErrorCtrl.error_404('View')
        else:
            ErrorCtrl.error_400()
