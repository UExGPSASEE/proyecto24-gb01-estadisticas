from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection

from clients.contenidos_client import ContenidosClient
from models.content import ContentType
from database import get_next_sequence_value as get_next_sequence_value
from models.review import Review
from controllers.error_ctrl import ErrorCtrl


class ReviewCtrl:
    @staticmethod
    def render_template(db: Collection):
        reviewsReceived = db.find()
        content_types = [(ct.name, ct.value) for ct in ContentType]
        return render_template('DB_Review.html', reviews=reviewsReceived, content_types=content_types)

    @staticmethod
    def addReview(db: Collection):
        idReview = get_next_sequence_value(db, "idReview")
        rating = request.form.get('rating')
        commentary = request.form.get('commentary')
        idProfile = request.form.get('idProfile')
        idContent = request.form.get('idContent')
        contentType = request.form.get('contentType')

        if idReview and idContent:
            if ContenidosClient.checkContentExists(int(idContent), int(contentType)):
                if not commentary:
                    commentary = None
                review = Review(int(idReview), int(rating), commentary, int(idProfile), int(idContent),
                                int(contentType))
                db.insert_one(review.toDBCollection())
                return redirect(url_for('reviews'))
            else:
                ErrorCtrl.error_404('Review')
        else:
            return jsonify({'error': 'Error when creating review', 'status': '500 Internal Server Error'}), 500

    @staticmethod
    def putReview(db: Collection, idReview: int):
        rating = request.form['rating']
        commentary = request.form['commentary']
        if idReview:
            idReview = int(idReview)
            filter = {'idReview': idReview}

            updateFields = {}

            if rating:
                updateFields['rating'] = rating
            if commentary:
                updateFields['commentary'] = commentary
            result = db.update_one(filter, updateFields)
            if result.matched_count == 0:
                ErrorCtrl.error_404('Review')
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
            idReview = int(idReview)
            result = db.delete_one({'idReview': idReview})
            if result.deleted_count == 1:
                return redirect(url_for('reviews'))
            else:
                ErrorCtrl.error_404('Review')
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
        reviewList = [
            {
                'idReview': review.get('idReview'),
                'rating': review.get('rating'),
                'commentary': review.get('commentary'),
                'idProfile': review.get('idProfile'),
                'idContent': review.get('idContent')
            }
            for review in allReviews
        ]
        if reviewList.__len__() > 0:
            return jsonify(reviewList), 200
        else:
            ErrorCtrl.error_404('Review')

    @staticmethod
    def getReviewById(db: Collection, idReview):
        if idReview:
            idReview = int(idReview)
            matching_review = db.find({'idReview': idReview})
            reviewFound = [
                {
                    'idReview': review.get('idReview'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'idProfile': review.get('idProfile'),
                    'idContent': review.get('idContent')
                }
                for review in matching_review
            ]
            if reviewFound.__len__()>0:
                return jsonify(reviewFound), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsByIdContent(db: Collection):
        idContent = request.args.get('idContent')
        if idContent:
            idContent = int(idContent)
            matching_review = db.find({'idContent': idContent})
            reviewList = [
                {
                    'idReview': review.get('idReview'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'idProfile': review.get('idProfile'),
                    'idContent': review.get('idContent')
                }
                for review in matching_review
            ]
            if reviewList.__len__() > 0:
                return jsonify(reviewList), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsByIdProfile(db: Collection):
        idProfile = request.args.get('idProfile')
        if idProfile:
            idProfile = int(idProfile)
            matching_review = db.find({'idProfile': idProfile})
            reviewList = [
                {
                    'idReview': review.get('idReview'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'idProfile': review.get('idProfile'),
                    'idContent': review.get('idContent')
                }
                for review in matching_review
            ]
            if reviewList.__len__() > 0:
                return jsonify(reviewList), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsByRating(db: Collection):
        rating = int(request.args.get('idRating'))
        if rating:
            matching_review = db.find({'rating': rating})
            reviewList = [
                {
                    'idReview': review.get('idReview'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'idProfile': review.get('idProfile'),
                    'idContent': review.get('idContent')
                }
                for review in matching_review
            ]
            if reviewList.__len__() > 0:
                return jsonify(reviewList), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsByMinRating(db: Collection):
        rating = int(request.args.get('rating'))
        if rating:
            matching_review = db.find({'rating': {'$gte': rating}})
            reviewList = [
                {
                    'idReview': review.get('idReview'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'idProfile': review.get('idProfile'),
                    'idContent': review.get('idContent')
                }
                for review in matching_review
            ]
            if reviewList.__len__() > 0:
                return jsonify(reviewList), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsByMaxRating(db: Collection):
        rating = int(request.args.get('rating'))
        if rating:
            matching_review = db.find({'rating': {'$lte': rating}})
            reviewList = [
                {
                    'idReview': review.get('idReview'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'idProfile': review.get('idProfile'),
                    'idContent': review.get('idContent')
                }
                for review in matching_review
            ]
            if reviewList.__len__() > 0:
                return jsonify(reviewList), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def getReviewsWithCommentary(db: Collection):
        allReviewsCommented = db.find({'commentary': {'$exists': True, '$ne': None}})
        reviewList = [
            {
                'idReview': review.get('idReview'),
                'rating': review.get('rating'),
                'commentary': review.get('commentary'),
                'idProfile': review.get('idProfile'),
                'idContent': review.get('idContent')
            }
            for review in allReviewsCommented
        ]
        return jsonify(reviewList), 200

    @staticmethod
    def getReviewsWithoutCommentary(db: Collection):
        allReviewsNotCommented = db.find({'commentary': None})
        reviewList = [
            {
                'idReview': review.get('idReview'),
                'rating': review.get('rating'),
                'commentary': review.get('commentary'),
                'idProfile': review.get('idProfile'),
                'idContent': review.get('idContent')
            }
            for review in allReviewsNotCommented
        ]
        return jsonify(reviewList), 200

    @staticmethod
    def getStatsReview(db: Collection):
        idContent = request.args.get('idContent')
        if idContent:
            idContent = int(idContent)
            matching_review = db.find({'idContent': idContent})
            reviewList = [
                {
                    'idReview': review.get('idReview'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'idProfile': review.get('idProfile'),
                    'idContent': review.get('idContent')
                }
                for review in matching_review
            ]
            if reviewList.__len__() > 0:
                return jsonify(reviewList), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400
