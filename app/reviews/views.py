"""Demonstrate all business reviews related API endpoints.

This module provides API endpoints to add business
reviews and view reviews fo a single business.

"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api

from app.models import Business, Reviews, User


class BusinessReviews(Resource):

    """Illustrate API endpoints to add and view business reviews."""

    @jwt_required
    def post(self, business_id):
        """Add a business review.
        ---
        tags:
            -   business reviews
        parameters:
            -   in: path
                name: business id
                required: true
                description: a unique business id
                schema:
                    type: integer
            -   in: header
                name: authorization
                description: JSON Web Token
                type: string
                required: true
                x-authentication: Bearer
            -   in: body
                name: review
                required: true
                schema:
                    required:
                        - review
                    properties:
                        review:
                            type: string
                            description: Business review
        responses:
            201:
                description: Review added
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
            404:
                description: Business is not registered
                schema:
                    properties:
                        response_message:
                            type: string
            500:
                description: Internal server error
                schema:
                    properties:
                        response_message:
                            type: string
        """
        request_data = request.get_json(force=True)
        business_review = request_data.get('review')
        created_by = get_jwt_identity()

        if not business_id:
            response = jsonify({
                'response_message': 'Business not registered!',
                'status_code': 404
            })
            return response
        if not business_review:
            response = jsonify({
                'response_message': 'Review field is required!',
                'status_code': 406})
            return response

        business = Business.query.filter_by(id=business_id).first()

        if business:
            try:
                reviewer_name = User.query.filter_by(id=created_by).first()
                review = Reviews(business_review, business_id, created_by)
                review.save()

                response = jsonify({
                    'reviewed_by': reviewer_name.username,
                    'review': business_review
                })
                return response
            except Exception as error:
                response = jsonify({
                    'response_message': str(error),
                    'status_code': 500})
                return response
        else:
            response = jsonify({
                'response_message': 'Business not registered!',
                'status_code': 404
            })
            return response

    @jwt_required
    def get(self, business_id):
        """View reviews for a business.
        ---
        tags:
            -   business reviews
        parameters:
            -   in: path
                name: business_id
                required: true
                type: integer
                description: a unique business id
            -   in: header
                name: authorization
                description: JSON Web Token
                type: string
                required: true
                x-authentication: Bearer
        responses:
            200:
                description: A dictionary of business reviews
                schema:
                    properties:
                        id:
                            type: integer
                            description: a unique review id
                        review:
                            type: string
                            description: a business review
                        reviewed_by:
                            type: integer
                            description: user id of the user who reviewed
            404:
                description: Business is not registered
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
            204:
                description: Business have not reviews
                schema:
                    properties:
                        response_message:
                            type: string
            500:
                description: Internal server error
                schema:
                    properties:
                        response_message:
                            type: string

        """
        if not business_id:
            return 404
        business = Business.query.filter_by(id=business_id).first()
        if business is None:
            response = jsonify({
                'response_message': 'Business id is not registered!',
                'status_code': 404
            })
            return response
        business_reviews = Reviews.query.filter_by(
            review_for=business_id).all()

        if business_reviews:
            try:
                _reviews = []

                for _review in business_reviews:
                    reviewer = User.query.filter_by(
                        id=_review.reviewed_by).first()
                    _object = {
                        'review': _review.review,
                        'reviewed_by': reviewer.username,
                    }
                    _reviews.append(_object)
                response = jsonify(reviews_list=_reviews)

                response.status_code = 200
                return response
            except Exception as error:
                response = jsonify({
                    'response_message': str(error),
                    'status_code': 500
                })
                return response
        else:
            response = jsonify({
                'response_message': 'Business have no reviews!',
                'status_code': 204
            })
            response.status_code = 404
            return response


reviews_api = Blueprint('reviews.views', __name__)
api = Api(reviews_api)
api.add_resource(BusinessReviews,
                 '/businesses/<int:business_id>/reviews', endpoint='reviews')
