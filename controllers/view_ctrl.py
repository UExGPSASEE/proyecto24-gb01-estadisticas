from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection
from models.views import View

class ViewsCtrl:
    @staticmethod
    def render_template(db: Collection):
        viewsReceived = db.find()
        return render_template('DB_Views.html', views=viewsReceived)
    
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
    def addView(db: Collection):
        idView = ViewsCtrl.get_next_sequence_value(db,"idView")
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