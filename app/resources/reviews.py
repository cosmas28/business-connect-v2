"""Demonstrate all business reviews related API endpoints.

This module provides API endpoints to add business reviews and view reviews fo a single business.

"""

import datetime
from flask import Blueprint, abort, request

from flask_restful import (Resource, Api, reqparse)

from app.models.reviews import Reviews


reviews = Reviews()


class BusinessReviews(Resource):

    """Illustrate API endpoints to add and view business reviews."""

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
        request_data = request.get_json()
        business_review = request_data['review']
        created_at = datetime.datetime.now().strftime("%y-%m-%d")

        response = reviews.add_review(business_id, business_review, created_at)
        return response, 201

    def get(self, business_id):
        """View reviews for a business using business by id.

        Args:
            business_id (int): business id parameter should be unique to identify each business.

        Returns:
            A json record of the business reviews.

        """
        response = reviews.view_business_reviews(business_id)

        return response, 200


reviews_api = Blueprint('resources.reviews', __name__)
api = Api(reviews_api)
api.add_resource(
    BusinessReviews,
    '/businesses/<int:business_id>/reviews',
    endpoint='reviews'
)
