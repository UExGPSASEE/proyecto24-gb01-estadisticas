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
        reviews_received = db.find()
        content_types = [(ct.name, ct.value) for ct in ContentType]
        return render_template('DB_Review.html', reviews=reviews_received, content_types=content_types)

    @staticmethod
    def add_review(db: Collection):
        id_review = get_next_sequence_value(db, "id_review")
        rating = request.form.get('rating')
        commentary = request.form.get('commentary')
        id_profile = request.form.get('id_profile')
        id_content = request.form.get('id_content')
        content_type = request.form.get('content_type')

        if id_review and id_content:
            if ContenidosClient.check_content_exists(int(id_content), int(content_type)):
                if not commentary:
                    commentary = None
                review = Review(int(id_review), int(rating), commentary, int(id_profile), int(id_content),
                                int(content_type))
                db.insert_one(review.toDBCollection())
                return redirect(url_for('reviews'))
            else:
                ErrorCtrl.error_404('Review')
        else:
            return jsonify({'error': 'Error when creating review', 'status': '500 Internal Server Error'}), 500

    @staticmethod
    def put_review(db: Collection, id_review: int):
        rating = request.form['rating']
        commentary = request.form['commentary']
        if id_review:
            id_review = int(id_review)
            filter = {'id_review': id_review}

            update_fields = {}

            if rating:
                update_fields['rating'] = rating
            if commentary:
                update_fields['commentary'] = commentary
            result = db.update_one(filter, update_fields)
            if result.matched_count == 0:
                ErrorCtrl.error_404('Review')
            elif result.modified_count == 0:
                return jsonify({'message': 'New review matches with actual review', 'status': '200 OK'}), 200
            return redirect(url_for('reviews'))
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def put_review_param(db: Collection):
        id_review = int(request.args.get('id_review'))
        return ReviewCtrl.put_review(db, id_review)

    @staticmethod
    def put_review_form(db: Collection):
        id_review = int(request.form.get('id_review'))
        return ReviewCtrl.put_review(db, id_review)

    @staticmethod
    def delete_review(db: Collection, id_review: int):
        if id_review:
            id_review = int(id_review)
            result = db.delete_one({'id_review': id_review})
            if result.deleted_count == 1:
                return redirect(url_for('reviews'))
            else:
                ErrorCtrl.error_404('Review')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def delete_review_param(db: Collection):
        id_review = int(request.args.get('id_review'))
        return ReviewCtrl.delete_review(db, id_review)

    @staticmethod
    def delete_review_form(db: Collection):
        id_review = int(request.form.get('id_review'))
        return ReviewCtrl.delete_review(db, id_review)

    @staticmethod
    def get_all_reviews(db: Collection):
        all_reviews = db.find()
        review_list = [
            {
                'id_review': review.get('id_review'),
                'rating': review.get('rating'),
                'commentary': review.get('commentary'),
                'id_profile': review.get('id_profile'),
                'id_content': review.get('id_content')
            }
            for review in all_reviews
        ]
        if review_list.__len__() > 0:
            return jsonify(review_list), 200
        else:
            ErrorCtrl.error_404('Review')

    @staticmethod
    def get_review_by_id(db: Collection, id_review):
        if id_review:
            id_review = int(id_review)
            matching_review = db.find({'id_review': id_review})
            review_found = [
                {
                    'id_review': review.get('id_review'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'id_profile': review.get('id_profile'),
                    'id_content': review.get('id_content')
                }
                for review in matching_review
            ]
            if review_found.__len__()>0:
                return jsonify(review_found), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def get_reviews_by_id_content(db: Collection):
        id_content = request.args.get('id_content')
        if id_content:
            id_content = int(id_content)
            matching_review = db.find({'id_content': id_content})
            review_list = [
                {
                    'id_review': review.get('id_review'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'id_profile': review.get('id_profile'),
                    'id_content': review.get('id_content')
                }
                for review in matching_review
            ]
            if review_list.__len__() > 0:
                return jsonify(review_list), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def get_reviews_by_id_profile(db: Collection):
        id_profile = request.args.get('id_profile')
        if id_profile:
            id_profile = int(id_profile)
            matching_review = db.find({'id_profile': id_profile})
            review_list = [
                {
                    'id_review': review.get('id_review'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'id_profile': review.get('id_profile'),
                    'id_content': review.get('id_content')
                }
                for review in matching_review
            ]
            if review_list.__len__() > 0:
                return jsonify(review_list), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def get_reviews_by_rating(db: Collection):
        rating = int(request.args.get('id_rating'))
        if rating:
            matching_review = db.find({'rating': rating})
            review_list = [
                {
                    'id_review': review.get('id_review'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'id_profile': review.get('id_profile'),
                    'id_content': review.get('id_content')
                }
                for review in matching_review
            ]
            if review_list.__len__() > 0:
                return jsonify(review_list), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def get_reviews_by_min_rating(db: Collection):
        rating = int(request.args.get('rating'))
        if rating:
            matching_review = db.find({'rating': {'$gte': rating}})
            review_list = [
                {
                    'id_review': review.get('id_review'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'id_profile': review.get('id_profile'),
                    'id_content': review.get('id_content')
                }
                for review in matching_review
            ]
            if review_list.__len__() > 0:
                return jsonify(review_list), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def get_reviews_by_max_rating(db: Collection):
        rating = int(request.args.get('rating'))
        if rating:
            matching_review = db.find({'rating': {'$lte': rating}})
            review_list = [
                {
                    'id_review': review.get('id_review'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'id_profile': review.get('id_profile'),
                    'id_content': review.get('id_content')
                }
                for review in matching_review
            ]
            if review_list.__len__() > 0:
                return jsonify(review_list), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            ErrorCtrl.error_400()

    @staticmethod
    def get_reviews_with_commentary(db: Collection):
        all_reviews_commented = db.find({'commentary': {'$exists': True, '$ne': None}})
        review_list = [
            {
                'id_review': review.get('id_review'),
                'rating': review.get('rating'),
                'commentary': review.get('commentary'),
                'id_profile': review.get('id_profile'),
                'id_content': review.get('id_content')
            }
            for review in all_reviews_commented
        ]
        return jsonify(review_list), 200

    @staticmethod
    def get_reviews_without_commentary(db: Collection):
        all_reviews_not_commented = db.find({'commentary': None})
        review_list = [
            {
                'id_review': review.get('id_review'),
                'rating': review.get('rating'),
                'commentary': review.get('commentary'),
                'id_profile': review.get('id_profile'),
                'id_content': review.get('id_content')
            }
            for review in all_reviews_not_commented
        ]
        return jsonify(review_list), 200

    @staticmethod
    def get_stats_review(db: Collection):
        id_content = request.args.get('id_content')
        if id_content:
            id_content = int(id_content)
            matching_review = db.find({'id_content': id_content})
            review_list = [
                {
                    'id_review': review.get('id_review'),
                    'rating': review.get('rating'),
                    'commentary': review.get('commentary'),
                    'id_profile': review.get('id_profile'),
                    'id_content': review.get('id_content')
                }
                for review in matching_review
            ]
            if review_list.__len__() > 0:
                return jsonify(review_list), 200
            else:
                ErrorCtrl.error_404('Review')
        else:
            ErrorCtrl.error_400()
