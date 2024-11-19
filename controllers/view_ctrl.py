from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection
from models.views import View
from database import get_next_sequence_value as get_next_sequence_value
import matplotlib as plt
import io

class ViewsCtrl:
    @staticmethod
    def render_template(db: Collection):
        viewsReceived = db.find()
        return render_template('DB_Views.html', views=viewsReceived)

    @staticmethod
    def addView(db: Collection):
        idView = get_next_sequence_value(db,"idView")
        dateInit = request.form['dateInit']
        dateFinish = request.form['dateFinish']
        idContent = request.form['idContent']
        idProfile = request.form['idProfile']

        if idView:
            if dateFinish:
                view = View(idView, dateInit, True, dateFinish, idContent, idProfile)
                db.insert_one(view.toDBCollection())
                return redirect(url_for('views'))
            else:
                view = View(idView, dateInit, False, None, idContent, idProfile)
                db.insert_one(view.toDBCollection())
                return redirect(url_for('views'))
        else:
            return jsonify({'error': 'View not found or not added', 'status':'404 Not Found'}), 404

    @staticmethod
    def putView(db: Collection):
        idView = int(request.form.get('idView'))
        dateFinish = request.form.get('dateFinish')
        if idView and dateFinish and (request.form.get('method') == 'PUT'):
            filter = {'idView': idView}
            change = {'$set': {'isFinished': True, 'dateFinish': dateFinish}}
            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'View not found or not updated', 'status':'404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'New view matches with actual view', 'status': '200 OK'}), 200
            return redirect(url_for('views'))
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteView(db: Collection):
        idView = int(request.form.get('idView'))
        if request.form.get('method') == 'DELETE' and idView:
            result = db.delete_one({'idView': idView})
            if result.deleted_count == 1:
                return redirect(url_for('views'))
            else:
                return jsonify({'error': 'View not found or not deleted', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400
           
    @staticmethod
    def getAllViews(db: Collection):
        allViews = db.find()
        view_list = [
            {
                'idView' : view.get('idView'),
                'dateInit' : view.get('dateInit'),
                'isFinished' : view.get('isFinished'),
                'dateFinish' : view.get('dateFinish'),
                'idContent' : view.get('idContent'),
                'idProfile' : view.get('idProfile')
            }
            for view in allViews
        ]
        return jsonify(view_list), 200
        
    @staticmethod
    def getViewById(db: Collection):
        idView = int(request.args.get('idView'))
        if idView:
            matching_view = db.find({'idView': idView})
            if matching_view:
                viewFound = [
                {
                    'idView' : view.get('idView'),
                    'dateInit' : view.get('dateInit'),
                    'isFinished' : view.get('isFinished'),
                    'dateFinish' : view.get('dateFinish'),
                    'idContent' : view.get('idContent'),
                    'idProfile' : view.get('idProfile')
                }
                for view in matching_view
                ]
                return jsonify(viewFound), 200
            else:
                return jsonify({'error': 'View not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400
        
    @staticmethod
    def getViewsByIdContent(db: Collection):
        idContent = request.args.get('idContent')
        if idContent:
            matching_view = db.find({'idContent': idContent})
            if matching_view:
                view_list = [
                {
                    'idView' : view.get('idView'),
                    'dateInit' : view.get('dateInit'),
                    'isFinished' : view.get('isFinished'),
                    'dateFinish' : view.get('dateFinish'),
                    'idContent' : view.get('idContent'),
                    'idProfile' : view.get('idProfile')
                }
                for view in matching_view
                ]
                return jsonify(view_list), 200
            else:
                return jsonify({'error': 'View not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400
        
    @staticmethod
    def getViewsByIdProfile(db: Collection):
        idProfile = request.args.get('idProfile')
        if idProfile:
            matching_view = db.find({'idProfile': idProfile})
            if matching_view:
                view_list = [
                {
                    'idView' : view.get('idView'),
                    'dateInit' : view.get('dateInit'),
                    'isFinished' : view.get('isFinished'),
                    'dateFinish' : view.get('dateFinish'),
                    'idContent' : view.get('idContent'),
                    'idProfile' : view.get('idProfile')
                }
                for view in matching_view
                ]
                return jsonify(view_list), 200
            else:
                return jsonify({'error': 'View not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400
        
    @staticmethod
    def getStatsView(db: Collection):
        idContent = request.args.get('idContent')
        if idContent:
            matching_view = db.find({'idContent': idContent})
            if matching_view:
                view_list = [
                {
                    'idView' : view.get('idView'),
                    'dateInit' : view.get('dateInit'),
                    'isFinished' : view.get('isFinished'),
                    'dateFinish' : view.get('dateFinish'),
                    'idContent' : view.get('idContent'),
                    'idProfile' : view.get('idProfile')
                }
                for view in matching_view
                ]
                return jsonify(len(view_list)), 200
            else:
                return jsonify({'error': 'View not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400
        