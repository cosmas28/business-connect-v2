"""Demonstrate all business related API endpoints.

This module provides API endpoints to register business,
view a single business, view all businesses.

"""

import re

from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api
from sqlalchemy import desc

from app.models import Business, Reviews
from app.models import User
from app.models import db
from app.utils import business_name_registered, get_paginated_list


class Businesses(Resource):

    """Illustrate API endpoints to register and view businesses."""

    @jwt_required
    def post(self):
        """Register a business.
        ---
        tags:
            -   businesses
        parameters:
            -   in: header
                name: authorization
                description: JSON Web Token
                type: string
                required: true
                x-authentication: Bearer
            -   in: body
                name: body
                schema:
                    id: Business
                    required:
                        - name
                        - category
                        - location
                        - summary
                    properties:
                        name:
                            type: string
                            description: Unique business name
                        category:
                            type: string
                            description: businesses with the same features
                        location:
                            type: string
                            description: Business physical location
                        summary:
                            type: string
                            description: Describes the business
        responses:
            201:
                description: Business has been registered successfully!
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
            406:
                description: Violate business column constraints
                schema:
                    properties:
                        response_message:
                            type: string
        """
        req_data = request.get_json(force=True)
        business_name = re.sub(r'\s+', '', str(req_data.get('name'))).lower()
        business_category = req_data.get('category')
        business_location = req_data.get('location')
        business_summary = req_data.get('summary')
        created_by = get_jwt_identity()

        if not business_name or not business_summary:
            response = jsonify({
               'response_message':
               'Business name and description are required!',
               'status_code': 406
            })
            return response
        if not business_location or not business_category:
            response = jsonify({
                'response_message':
                    'Business location and category are required!',
                'status_code': 406
            })
            return response
        if not business_name_registered(business_name):
            try:
                business = Business(business_name, business_category,
                                    business_location,
                                    business_summary, created_by)
                business.save()

                response = jsonify({
                    'response_message':
                        'Business has been registered successfully!',
                    'status_code': 201
                })
                return response
            except Exception as error:
                response_message = {
                    'message': str(error),
                    'status_code': 500}
                return make_response(jsonify(response_message))
        else:
            response = jsonify({
                'response_message': 'Business name already registered!',
                'status_code': 406
            })
            return response

    @jwt_required
    def get(self):
        """View all registered businesses.
        ---
        tags:
            -   businesses
        parameters:
            -   in: header
                name: authorization
                description: JSON Web Token
                type: string
                required: true
                x-authentication: Bearer
        responses:
            200:
                description: A list of dictionaries of businesses
                schema:
                    properties:
                        business_list:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        description: a unique business id
                                    name:
                                        type: string
                                        description: a unique business name
                                    category:
                                        type: string
                                        description: used to group businesses
                                    location:
                                        type: string
                                        description: business location
                                    summary:
                                        type: string
                                        description: business description
                                    created_by:
                                        type: integer
                                        description: id of the business owner
            500:
                description: Internal server error
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
            security:
                BearAuth:
                    securitySchemes:
                        type: http
                        scheme: bearer
                        bearerFormat: JWT

        """

        try:
            # businesses = Business.query.all()
            businesses = Business.query.order_by(desc(Business.id)).all()
            business_result = []

            for business in businesses:
                _object = {
                    'id': business.id,
                    'name': business.name,
                    'category': business.category,
                    'location': business.location,
                    'summary': business.summary,
                    'created_by': business.created_by
                }
                business_result.append(_object)

            response = jsonify(business_list=business_result)
            response.status_code = 200
            return response
        except Exception as e:
            response = jsonify({
                'response_message': str(e),
                'status_code': 500
            })
            return response


class OneBusiness(Resource):

    """Illustrate API endpoints to manipulate single business."""

    @jwt_required
    def get(self, business_id):
        """view a registered business by id.
        ---
        tags:
            -   businesses
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
        responses:
            200:
                description: A dictionary of business data
                schema:
                    properties:
                        id:
                            type: integer
                            description: a unique business id
                        name:
                            type: string
                            description: a unique business name
                        category:
                            type: string
                            description: used to group businesses
                        location:
                            type: string
                            description: describes physical location
                        summary:
                            type: string
                            description: business description
                        created_by:
                            type: string
                            description: username of the business owner
                        owner_id:
                            type: integer
                            description: describes the id of the business owner
                        reviews:
                            type: array
                            items:
                                type: string
                                description: a list of business reviews
            404:
                description: Business is not registered
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
            500:
                description: Internal server error
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
        """

        business = Business.query.filter_by(id=business_id).first()
        if business:
            user_id = business.created_by
            user = User.query.filter_by(id=user_id).first()
            reviews = Reviews.query.filter_by(review_for=business_id).all()
            _reviews = []

            for _review in reviews:
                reviewer = User.query.filter_by(
                    id=_review.reviewed_by).first()
                _object = {
                    'review': _review.review,
                    'reviewed_by': reviewer.username,
                }
                _reviews.append(_object)
            try:
                business_object = jsonify({
                    'id': business.id,
                    'name': business.name,
                    'category': business.category,
                    'location': business.location,
                    'summary': business.summary,
                    'created_by': user.username,
                    'owner_id': business.created_by,
                    'reviews': _reviews
                })

                business_object.status_code = 200
                return business_object
            except Exception as e:
                response = jsonify({
                    'response_message': str(e),
                    'status_code': 500
                })
                return response
        else:
            response = jsonify({
                'response_message': 'Business id is not registered!',
                'status_code': 404
            })
            return response

    @jwt_required
    def put(self, business_id):
        """Update a registered business.
        ---
        tags:
            -   businesses
        parameters:
            -   in: path
                name: business_id
                required: true
                schema:
                    type: integer
            -   in: header
                name: authorization
                description: JSON Web Token
                type: string
                required: true
                x-authentication: Bearer
            -   in: body
                name: new data
                description: new business data
                schema:
                    id: Business
                    properties:
                        name:
                            type: string
                            description: Unique business name
                        category:
                            type: string
                            description: businesses with the same features
                        location:
                            type: string
                            description: Business physical location
                        summary:
                            type: string
                            description: Describes the business
        responses:
            200:
                description: A dictionary of business data
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
                        status_code:
                            type: integer
            500:
                description: Internal server error
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
        """

        req_data = request.get_json(force=True)
        business_name = req_data.get('name')
        business_category = req_data.get('category')
        business_location = req_data.get('location')
        business_summary = req_data.get('summary')

        business_is_registered = Business.query.filter_by(
            id=business_id).first()
        if business_is_registered:
            try:
                Business.query.filter_by(id=business_id).update(dict(
                    name=business_name,
                    category=business_category,
                    location=business_location,
                    summary=business_summary
                ))
                db.session.commit()

                response = jsonify({
                    'response_message':
                        'Business has been updated successfully!',
                        'status_code': 200
                })
                response.status_code = 200
                return response
            except Exception as e:
                response = jsonify({
                    'response_message': str(e),
                    'status_code': 500
                })
                return response
        else:
            response = jsonify({
                'response_message': 'Business id is not registered!',
                'status_code': 404
            })
            return response

    @jwt_required
    def delete(self, business_id):
        """Delete a registered business.
        ---
        tags:
            -   businesses
        parameters:
            -   in: path
                name: business_id
                required: true
                schema:
                    type: integer
            -   in: header
                name: authorization
                description: JSON Web Token
                type: string
                required: true
                x-authentication: Bearer
        responses:
            204:
                description: successful delete message
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
                        status_code:
                            type: integer
            401:
                description: Permission required
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
            500:
                description: Internal server error
                schema:
                    properties:
                        response_message:
                            type: strin
                        status_code:
                            type: integer
        """

        created_by = get_jwt_identity()
        business = Business.query.filter_by(id=business_id).first()
        if business is None:
            response = jsonify({
                'response_message': 'Business id is not registered!',
                'status_code': 404
            })
            return response

        if business.created_by == created_by:
            try:
                business = Business.query.filter_by(id=business_id).first()

                db.session.delete(business)
                db.session.commit()
                response = jsonify({
                    'response_message':
                        'Business has been deleted successfully!',
                        'status_code': 204
                })
                return response
            except Exception as e:
                response = jsonify({
                    'response_message': str(e),
                    'status_code': 500
                })
                return response
        else:
            response = jsonify({
                'response_message':
                    'Permission required to delete this business!',
                'status_code': 401
            })
            return response


class UserBusiness(Resource):

    """Illustrate API endpoints to manipulate one user business."""

    @jwt_required
    def get(self, user_id):
        """view a registered business by user id.
        ---
        tags:
            -   businesses
        parameters:
            -   in: path
                name: user id
                required: true
                description: a unique user id
                schema:
                    type: integer
            -   in: header
                name: authorization
                description: JSON Web Token
                type: string
                required: true
                x-authentication: Bearer
        responses:
            200:
                description: A dictionary of business data
                schema:
                    properties:
                        business_list:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        description: a unique business id
                                    name:
                                        type: string
                                        description: a unique business name
                                    category:
                                        type: string
                                        description: used to group businesses
                                    location:
                                        type: string
                                        description: describes physical location
                                    summary:
                                        type: string
                                        description: business description
                                    created_by:
                                        type: string
                                        description: username of the business owner
            404:
                description: User is not registered
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
            500:
                description: Internal server error
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
        """
        user = User.query.filter_by(id=user_id).first()
        if user:
            businesses = Business.query.filter_by(created_by=user_id).all()
            if businesses:
                try:
                    business_result = []

                    for business in businesses:
                        _object = {
                            'id': business.id,
                            'name': business.name,
                            'category': business.category,
                            'location': business.location,
                            'summary': business.summary,
                            'created_by': user.username
                        }
                        business_result.append(_object)

                    response = jsonify(business_list=business_result)
                    response.status_code = 200
                    return response
                except Exception as e:
                    response = jsonify({
                        'response_message': str(e),
                        'status_code': 500
                    })
                    return response
            else:
                response = jsonify({
                    'response_message': 'You have not registered a business!',
                    'status_code': 204
                })
                response.status_code = 204
                return response
        else:
            response = jsonify({
                'response_message': 'User is not registered!',
                'status_code': 404
            })
            return response


class SearchBusiness(Resource):

    """Illustrate API endpoints to search businesses."""

    @jwt_required
    def get(self):
        """Search a registered business.
        ---
        tags:
            -   businesses
        parameters:
            -   in: query
                name: name
                description: business name/category/location
                required: true
                schema:
                    type: string
            -   in: header
                name: authorization
                description: JSON Web Token
                type: string
                required: true
                x-authentication: Bearer
        responses:
            200:
                description: A list of dictionaries of businesses
                schema:
                    properties:
                        business_list:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        description: a unique business id
                                    name:
                                        type: string
                                        description: a unique business name
                                    category:
                                        type: string
                                        description: used to group businesses
                                    location:
                                        type: string
                                        description: physical location
                                    summary:
                                        type: string
                                        description: business description
                                    created_by:
                                        type: integer
                                        description: id of the business owner
            404:
                description: Business not found
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
            500:
                description: Internal server error
                schema:
                    properties:
                        response_message:
                            type: string
                        status_code:
                            type: integer
        """

        user_request = request.args.get('q').lower()
        found_businesses = []
        all_businesses = Business.query.all()
        for row in all_businesses:
            if row.name.startswith(user_request) or \
                row.category.startswith(user_request) or \
                    row.location.startswith(user_request):
                        found_businesses.append(row)
        if found_businesses:
            try:
                business_list = []

                for business in found_businesses:
                    _object = {
                        'id': business.id,
                        'name': business.name,
                        'category': business.category,
                        'location': business.location,
                        'summary': business.summary,
                        'created_by': business.created_by
                    }
                    business_list.append(_object)
                response = jsonify(business_list=business_list)
                response.status_code = 200
                return response
            except Exception as e:
                response = jsonify({
                    'response_message': str(e),
                    'status_code': 500
                })
                return response
        else:
            response = jsonify({
                'response_message': 'Business not found!',
                'status_code': 404
            })
            return response


business_api = Blueprint('business.views', __name__)
api = Api(business_api)
api.add_resource(Businesses, '/businesses', endpoint='businesses')
api.add_resource(OneBusiness,
                 '/businesses/<int:business_id>', endpoint='business')
api.add_resource(UserBusiness,
                 '/businesses/user/<int:user_id>', endpoint='user_business')
api.add_resource(SearchBusiness, '/businesses/search', endpoint='search')
