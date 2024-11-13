from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection
from models.views import Views

class ViewsCtrl:
    @staticmethod
    def render_template(db: Collection):
        viewsReceived = db.find()
        return render_template('DB_Views.html', views=viewsReceived)

    @staticmethod
    def addViews(db: Collection):
        name = request.form['name']

        if name:
            views = Views(name)
            db.insert_one(views.toDBCollection())
            return redirect(url_for('views'))
        else:
            return jsonify({'error': 'Views not found or not updated'}), 404

    @staticmethod
    def putViews(db: Collection):
        views = db['Views']
        actualName = request.form['actualName']
        name = request.form['name']

        if name and actualName:
            filter = {'Name': actualName}
            change = {'$set': {'Name': name}}
            result = views.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Views not found or not updated'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'Ya tiene ese nombre', 'status': '200 OK'}), 200
            return redirect(url_for('views'))
        else:
            return jsonify({'message': 'Faltan datos', 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteViews(db: Collection):
        views_name = request.form['name']
        db.delete_one({'name': views_name})
        if request.form.get('_method') == 'DELETE':
            views_name = request.form['name']
            result = db.delete_one({'name': views_name})
            if result.deleted_count == 1:
                print("Delete ok")
                return redirect(url_for('views'))
            else:
                print("Delete failed")
                return redirect(url_for('views'))
        else:
            return redirect(url_for('views'))