"""Demonstrate all business reviews related API endpoints.

This module provides API endpoints to add business reviews and view reviews fo a single business.

"""

from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api
from sqlalchemy import exc

from app.models import Business, Reviews
from app.models import db


class BusinessReviews(Resource):

    """Illustrate API endpoints to add and view business reviews."""

    @jwt_required
    def post(self, business_id):
        """Add a business review.
        ---
        tags:
            -   business reviews
        parameters:
            -   in: body
                name: body
                schema:
                    $ref: '#/definitions/User'
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            201:
                description: Created
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                response_message:
                                    type: string
                                    description: message to show review has been added successfully
        """
        request_data = request.get_json(force=True)
        business_review = request_data.get('review')
        created_by = get_jwt_identity()

        try:
            business = Business.query.filter_by(id=business_id).first()

            if len(str(business_id)) == 0:
                return 404
            if business is None:
                response = {
                    'response_message': 'Business not registered!'
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
        except exc.IntegrityError:
            response_text = 'Review field is required!'
            return {'response_message': response_text}, 406

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
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                id:
                                    type: integer
                                    description: a unique business id
                                review:
                                    type: string
                                    description: review description
                                reviewed_by:
                                    type: integer
                                    description: describes the id of the user who reviewed

        """
        try:
            business = Business.query.filter_by(id=business_id).first()
            business_reviews = Reviews.query.filter_by(review_for=business_id).all()
            if len(str(business_id)) == 0:
                return 404
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
                        'id': _review.id,
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


reviews_api = Blueprint('views.reviews', __name__)
api = Api(reviews_api)
api.add_resource(BusinessReviews, '/businesses/<int:business_id>/reviews', endpoint='reviews')
