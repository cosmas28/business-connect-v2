"""Demonstrate all business reviews related API endpoints.

This module provides API endpoints to add business reviews and view reviews fo a single business.

"""

from flask import Blueprint, request, make_response, jsonify

from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.models import Business, Reviews
from app.models import db


class BusinessReviews(Resource):

    """Illustrate API endpoints to add and view business reviews."""

    @jwt_required
    def post(self, business_id):
        """Add a business review.

        Args:
            business_id (int): business id parameter should be unique to identify each business.

        Returns:
            A success message to indicate review was added successfully.

        Raises:
            KeyError when the business id does not exist.
            Error message when business review is empty.
            Error message when no business id was provided.

        """
        request_data = request.get_json(force=True)
        business_review = request_data['review']
        created_by = get_jwt_identity()

        try:
            business = Business.query.filter_by(bid=business_id).first()

            if len(str(business_id)) == 0:
                response = {
                    'response_message': 'Business id is required!'
                }
                return make_response(jsonify(response))
            if business is None:
                response = {
                    'response_message': 'Business not registered!'
                }
                return make_response(jsonify(response))
            if len(business_review) == 0:
                response = {
                    'response_message': 'Review value is empty!'
                }
                return make_response(jsonify(response))
            else:
                review = Reviews(business_review, business_id, created_by)
                db.session.add(review)
                db.session.commit()

                response = {
                    'response_message': 'Review has been added successfully!'
                }

                return make_response(jsonify(response))
        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))

    @jwt_required
    def get(self, business_id):
        """View reviews for a business using business by id.

        Args:
            business_id (int): business id parameter should be unique to identify each business.

        Returns:
            A json record of the business reviews.

        """
        try:
            business = Business.query.filter_by(bid=business_id).first()
            business_reviews = Reviews.query.filter_by(review_for=business_id).all()
            if len(str(business_id)) == 0:
                response = {
                    'response_message': 'Business id is required!'
                }
                return make_response(jsonify(response))
            elif business is None:
                response = {
                    'response_message': 'Business id is not registered!'
                }
                return make_response(jsonify(response))
            elif business_reviews is None:
                response = {
                    'response_message': 'Business have no reviews!'
                }
                return make_response(jsonify(response))
            else:
                _reviews = []

                for _review in business_reviews:
                    _object = {
                        'id': _review.rid,
                        'review': _review.review,
                        'reviewed_by': _review.reviewed_by,
                    }
                    _reviews.append(_object)

                return make_response(jsonify(reviews_list=_reviews))
        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))


reviews_api = Blueprint('resources.reviews', __name__)
api = Api(reviews_api)
api.add_resource(
    BusinessReviews,
    '/businesses/<int:business_id>/reviews',
    endpoint='reviews'
)
