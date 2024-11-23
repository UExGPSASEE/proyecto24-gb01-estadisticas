from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from database import get_next_sequence_value as get_next_sequence_value
from models.review import Review


class ReviewCtrl:
    @staticmethod
    def render_template(db: Collection):
        reviewsReceived = db.find()
        return render_template('DB_Review.html', reviews=reviewsReceived)

    @staticmethod
    def addReview(db: Collection):
        idReview = get_next_sequence_value(db, "idReview")
        rating = request.form['rating']
        commentary = request.form['commentary']
        idProfileUser = request.form['idProfileUser']
        idContent = request.form['idContent']

        if idReview:
            if commentary:
                review = Review(idReview, int(rating), commentary, idProfileUser, idContent)
                db.insert_one(review.toDBCollection())
                return redirect(url_for('reviews'))
            else:
                review = Review(idReview, int(rating), None, idProfileUser, idContent)
                db.insert_one(review.toDBCollection())
                return redirect(url_for('reviews'))
        else:
            return jsonify({'error': 'Review not found or not added', 'status': '404 Not Found'}), 404

    @staticmethod
    def putReview(db: Collection, idReview: int):
        rating = request.form['rating']
        commentary = request.form['commentary']
        idProfileUser = request.form['idProfileUser']
        idContent = request.form['idContent']
        if idReview:
            filter = {'idReview': idReview}

            updateFields = {}

            if rating:
                updateFields['rating'] = rating
            if commentary:
                updateFields['commentary'] = commentary
            if idProfileUser:
                updateFields['idProfileUser'] = idProfileUser
            if idContent:
                updateFields['idContent'] = idContent

            result = db.update_one(filter, updateFields)
            if result.matched_count == 0:
                return jsonify({'error': 'Review not found or not updated', 'status': '404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'New review matches with actual review', 'status': '200 OK'}), 200
            return redirect(url_for('reviews'))
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def putReviewParam(db: Collection):
        idReview = int(request.args.get('idReview'))
        return ReviewCtrl.putReview(db, idReview)

    @staticmethod
    def putReviewForm(db: Collection):
        idReview = int(request.form.get('idReview'))
        return ReviewCtrl.putReview(db, idReview)

    @staticmethod
    def deleteReview(db: Collection, idReview: int):
        if idReview:
            result = db.delete_one({'idReview': idReview})
            if result.deleted_count == 1:
                return redirect(url_for('reviews'))
            else:
                return jsonify({'error': 'Review not found or not deleted', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteReviewParam(db: Collection):
        idReview = int(request.args.get('idReview'))
        return ReviewCtrl.deleteReview(db, idReview)

    @staticmethod
    def deleteReviewForm(db: Collection):
        idReview = int(request.form.get('idReview'))
        return ReviewCtrl.deleteReview(db, idReview)

    @staticmethod
    def getAllReviews(db: Collection):
        allReviews = db.find()
        review_list = [
            {
                'idReview': review.get('idReview'),
                'rating': review.get('rating'),
                'commentary': review.get('commentary'),
                'idProfileUser': review.get('idProfileUser'),
                'idContent': review.get('idContent')
            }
            for review in allReviews
        ]
        return jsonify(review_list), 200

    @staticmethod
    def getReviewById(db: Collection):
        idReview = int(request.args.get('idReview'))
        if idReview:
            matching_review = db.find({'idReview': idReview})
            if matching_review:
                reviewFound = [
                    {
                        'idReview': review.get('idReview'),
                        'rating': review.get('rating'),
                        'commentary': review.get('commentary'),
                        'idProfileUser': review.get('idProfileUser'),
                        'idContent': review.get('idContent')
                    }
                    for review in matching_review
                ]
                return jsonify(reviewFound), 200
            else:
                return jsonify({'error': 'Review not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsByIdContent(db: Collection):
        idContent = request.args.get('idContent')
        if idContent:
            matching_review = db.find({'idContent': idContent})
            if matching_review:
                review_list = [
                    {
                        'idReview': review.get('idReview'),
                        'rating': review.get('rating'),
                        'commentary': review.get('commentary'),
                        'idProfileUser': review.get('idProfileUser'),
                        'idContent': review.get('idContent')
                    }
                    for review in matching_review
                ]
                return jsonify(review_list), 200
            else:
                return jsonify({'error': 'Review not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsByIdProfile(db: Collection):
        idProfile = request.args.get('idProfileUser')
        if idProfile:
            matching_review = db.find({'idProfileUser': idProfile})
            if matching_review:
                review_list = [
                    {
                        'idReview': review.get('idReview'),
                        'rating': review.get('rating'),
                        'commentary': review.get('commentary'),
                        'idProfileUser': review.get('idProfileUser'),
                        'idContent': review.get('idContent')
                    }
                    for review in matching_review
                ]
                return jsonify(review_list), 200
            else:
                return jsonify({'error': 'Review not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsByRating(db: Collection):
        rating = int(request.args.get('rating'))
        if rating:
            matching_review = db.find({'rating': rating})
            if matching_review:
                review_list = [
                    {
                        'idReview': review.get('idReview'),
                        'rating': review.get('rating'),
                        'commentary': review.get('commentary'),
                        'idProfileUser': review.get('idProfileUser'),
                        'idContent': review.get('idContent')
                    }
                    for review in matching_review
                ]
                return jsonify(review_list), 200
            else:
                return jsonify({'error': 'Review not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsByMinRating(db: Collection):
        rating = int(request.args.get('rating'))
        if rating:
            matching_review = db.find({'rating': {'$gte': rating}})
            if matching_review:
                review_list = [
                    {
                        'idReview': review.get('idReview'),
                        'rating': review.get('rating'),
                        'commentary': review.get('commentary'),
                        'idProfileUser': review.get('idProfileUser'),
                        'idContent': review.get('idContent')
                    }
                    for review in matching_review
                ]
                return jsonify(review_list), 200
            else:
                return jsonify({'error': 'Review not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsByMaxRating(db: Collection):
        rating = int(request.args.get('rating'))
        if rating:
            matching_review = db.find({'rating': {'$lte': rating}})
            if matching_review:
                review_list = [
                    {
                        'idReview': review.get('idReview'),
                        'rating': review.get('rating'),
                        'commentary': review.get('commentary'),
                        'idProfileUser': review.get('idProfileUser'),
                        'idContent': review.get('idContent')
                    }
                    for review in matching_review
                ]
                return jsonify(review_list), 200
            else:
                return jsonify({'error': 'Review not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsWithCommentary(db: Collection):
        allReviewsCommented = db.find({'commentary': {'$exists': True, '$ne': None}})
        review_list = [
            {
                'idReview': review.get('idReview'),
                'rating': review.get('rating'),
                'commentary': review.get('commentary'),
                'idProfileUser': review.get('idProfileUser'),
                'idContent': review.get('idContent')
            }
            for review in allReviewsCommented
        ]
        return jsonify(review_list), 200

    @staticmethod
    def getReviewsWithoutCommentary(db: Collection):
        allReviewsNotCommented = db.find({'commentary': None})
        review_list = [
            {
                'idReview': review.get('idReview'),
                'rating': review.get('rating'),
                'commentary': review.get('commentary'),
                'idProfileUser': review.get('idProfileUser'),
                'idContent': review.get('idContent')
            }
            for review in allReviewsNotCommented
        ]
        return jsonify(review_list), 200

    @staticmethod
    def getStatsReview(db: Collection):
        idContent = request.args.get('idContent')
        if idContent:
            matching_review = db.find({'idContent': idContent})
            if matching_review:
                review_list = [
                    {
                        'idReview': review.get('idReview'),
                        'rating': review.get('rating'),
                        'commentary': review.get('commentary'),
                        'idProfileUser': review.get('idProfileUser'),
                        'idContent': review.get('idContent')
                    }
                    for review in matching_review
                ]
                return jsonify(len(review_list)), 200
            else:
                return jsonify({'error': 'Review not found', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400
