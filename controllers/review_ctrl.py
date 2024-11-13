from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection
from models.review import Review

class ReviewCtrl:
    @staticmethod
    def render_template(db: Collection):
        reviewsReceived = db.find()
        return render_template('DB_Review.html', reviews=reviewsReceived)

    @staticmethod
    def addReview(db: Collection):
        content_id = request.form['Content_id']
        valoracion = request.form['Valoracion']
        comentario = request.form['Comentario']
        profile = request.form['Profile']

        if profile:
            review = Review(content_id, valoracion, comentario, profile)
            db.insert_one(review.toDBCollection())
            return redirect(url_for('reviews'))
        else:
            return jsonify({'error': 'Review not found or not updated'}), 404

    @staticmethod
    def putReview(db: Collection):
        actualProfile = request.form['Profile']
        actualContent_id = request.form['Content_id']
        valoracion = request.form['Valoracion']
        comentario = request.form['Comentario']

        if actualProfile and actualContent_id and valoracion:
            filter = {'Profile': actualProfile, 'Content_id': actualContent_id}
            if comentario:
                change = {'$set': {'Profile': actualProfile, 'Content_id': actualContent_id, 'Valoracion': valoracion,
                                   'Comentario': comentario}}
            else:
                change = {'$set': {'Profile': actualProfile, 'Content_id': actualContent_id, 'Valoracion': valoracion}}
            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Review not found or not updated'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'Ya tiene esa valoracion y/o comentario', 'status': '200 OK'}), 200
            return redirect(url_for('reviews'))
        else:
            return jsonify({'message': 'Faltan datos', 'status': '400 Bad Request'}), 400


    @staticmethod
    def deleteReview(db: Collection):
        review_name = request.form['name']
        db.delete_one({'name': review_name})
        if request.form.get('_method') == 'DELETE':
            review_name = request.form['name']
            result = db.delete_one({'name': review_name})
            if result.deleted_count == 1:
                print("Delete ok")
                return redirect(url_for('reviews'))
            else:
                print("Delete failed")
                return redirect(url_for('reviews'))
        else:
            return redirect(url_for('reviews'))