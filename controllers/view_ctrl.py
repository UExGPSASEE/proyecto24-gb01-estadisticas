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
        viewsReceived = db.find()
        content_types = [(ct.name, ct.value) for ct in ContentType]
        return render_template('DB_Views.html', views=viewsReceived, content_types=content_types)

    @staticmethod
    def addView(db: Collection):
        idView = get_next_sequence_value(db, "idView")
        dateInit = request.form.get('dateInit')
        dateFinish = request.form.get('dateFinish')
        idProfile = request.form.get('idProfile')
        idContent = request.form.get('idContent')
        contentType = request.form.get('contentType')

        if idView and idContent:
            if ContenidosClient.checkContentExists(int(idContent), int(contentType)):
                if not dateFinish:
                    dateFinish = None
                    isFinished = False
                else:
                    isFinished = True

                view = View(idView, dateInit, isFinished, dateFinish, int(idProfile), int(idContent), int(contentType))
                db.insert_one(view.toDBCollection())
                return redirect(url_for('views'))

            else:
                ErrorCtrl.error_404('View')
        else:
            return jsonify({'error': 'Error when creating view', 'status': '500 Internal Server Error'}), 500

    @staticmethod
    def putView(db: Collection, idView: int):
        dateFinish = request.form.get('dateFinish')
        if idView and dateFinish:
            idView = int(idView)
            filter = {'idView': idView}
            change = {'$set': {'isFinished': True, 'dateFinish': dateFinish}}
            result = db.update_one(filter, change)
            if result.matched_count == 0:
                ErrorCtrl.error_404('View')
            elif result.modified_count == 0:
                return jsonify({'message': 'New view matches with actual view', 'status': '200 OK'}), 200
            return redirect(url_for('views'))
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def putViewParam(db: Collection):
        idView = int(request.args.get('idView'))
        return ViewsCtrl.putView(db, idView)

    @staticmethod
    def putViewForm(db: Collection):
        idView = int(request.form.get('idView'))
        return ViewsCtrl.putView(db, idView)

    @staticmethod
    def deleteView(db: Collection, idView: int):
        if idView:
            idView = int(idView)
            result = db.delete_one({'idView': idView})
            if result.deleted_count == 1:
                return redirect(url_for('views'))
            else:
                ErrorCtrl.error_404('View')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteViewParam(db: Collection):
        idView = int(request.args.get('idView'))
        return ViewsCtrl.deleteView(db, idView)

    @staticmethod
    def deleteViewForm(db: Collection):
        idView = int(request.form.get('idView'))
        return ViewsCtrl.deleteView(db, idView)

    @staticmethod
    def getAllViews(db: Collection):
        allViews = db.find()
        viewlist = [
            {
                'idView': view.get('idView'),
                'dateInit': view.get('dateInit'),
                'isFinished': view.get('isFinished'),
                'dateFinish': view.get('dateFinish'),
                'idContent': view.get('idContent'),
                'idProfile': view.get('idProfile')
            }
            for view in allViews
        ]
        if viewlist.__len__()>0:
            return jsonify(viewlist), 200
        else:
            ErrorCtrl.error_404('View')

    @staticmethod
    def getViewById(db: Collection, idView):
        if idView:
            idView = int(idView)
            matching_view = db.find({'idView': idView})
            if matching_view:
                viewList = [
                    {
                        'idView': view.get('idView'),
                        'dateInit': view.get('dateInit'),
                        'isFinished': view.get('isFinished'),
                        'dateFinish': view.get('dateFinish'),
                        'idContent': view.get('idContent'),
                        'idProfile': view.get('idProfile')
                    }
                    for view in matching_view
                ]

                if viewList.__len__() > 0:
                    return jsonify(viewList), 200
                else:
                    ErrorCtrl.error_404('View')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getViewsByIdContent(db: Collection):
        idContent = request.args.get('idContent')
        if idContent:
            idContent = int(idContent)
            matching_view = db.find({'idContent': idContent})
            viewList = [
                {
                    'idView': view.get('idView'),
                    'dateInit': view.get('dateInit'),
                    'isFinished': view.get('isFinished'),
                    'dateFinish': view.get('dateFinish'),
                    'idContent': view.get('idContent'),
                    'idProfile': view.get('idProfile')
                }
                for view in matching_view
            ]

            if viewList.__len__() > 0:
                return jsonify(viewList), 200
            else:
                ErrorCtrl.error_404('View')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getViewsByIdProfile(db: Collection):
        idProfile = request.args.get('idProfile')
        if idProfile:
            idProfile = int(idProfile)
            matching_view = db.find({'idProfile': idProfile})
            viewList = [
                {
                    'idView': view.get('idView'),
                    'dateInit': view.get('dateInit'),
                    'isFinished': view.get('isFinished'),
                    'dateFinish': view.get('dateFinish'),
                    'idContent': view.get('idContent'),
                    'idProfile': view.get('idProfile')
                }
                for view in matching_view
            ]

            if viewList.__len__() > 0:
                return jsonify(viewList), 200
            else:
                ErrorCtrl.error_404('View')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getStatsView(db: Collection):
        idContent = request.args.get('idContent')
        if idContent:
            idContent = int(idContent)
            matching_view = db.find({'idContent': idContent})
            viewList = [
                {
                    'idView': view.get('idView'),
                    'dateInit': view.get('dateInit'),
                    'isFinished': view.get('isFinished'),
                    'dateFinish': view.get('dateFinish'),
                    'idContent': view.get('idContent'),
                    'idProfile': view.get('idProfile')
                }
                for view in matching_view
            ]

            if viewList.__len__() > 0:
                return jsonify(viewList), 200
            else:
                ErrorCtrl.error_404('View')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400
