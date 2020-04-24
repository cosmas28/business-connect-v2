"""Demonstrate all business related API endpoints.

This module provides API endpoints to register business,
view a single business, view all businesses.

"""

import re

from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api

from app.models import Business
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
            406:
                description: Violate business column constraints
                schema:
                    properties:
                        response_message:
                            type: string
        """
        req_data = request.get_json(force=True)
        business_name = req_data.get('name')
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
                business_to_save = Business(business_name, business_category,
                                    business_location,
                                    business_summary, created_by)
                business_to_save.save()
                business = Business.query.filter_by(name=business_name).first()
                business_object = {
                        'id': business.id,
                        'name': business.name,
                        'category': business.category,
                        'location': business.location,
                        'summary': business.summary,
                        'created_by': business.created_by
                    }
                response = jsonify({
                    'response_message':
                        'Business has been registered successfully!',
                    'status_code': 201,
                    'data': business_object
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
                    name: business_list
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
                            type: integer
                            description: describes the id of the business owner
            500:
                description: Internal server error
                schema:
                    properties:
                        response_message:
                            type: string
            security:
                BearAuth:
                    securitySchemes:
                        type: http
                        scheme: bearer
                        bearerFormat: JWT

        """

        try:
            businesses = Business.query.all()
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
                            type: integer
                            description: describes the id of the business owner
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

        business = Business.query.filter_by(id=business_id).first()
        if business:
            try:
                business_object = jsonify({
                    'id': business.id,
                    'name': business.name,
                    'category': business.category,
                    'location': business.location,
                    'summary': business.summary,
                    'created_by': business.created_by
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
                            type: integer
                            description: describes the id of the business owner
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

                new_business = Business.query.filter_by(id=business_id).first()
                business_object = jsonify({
                    'message': 'Business successfuly updated!',
                    'status_code': 200,
                    'data': {
                        'id': new_business.id,
                        'name': new_business.name,
                        'category': new_business.category,
                        'location': new_business.location,
                        'summary': new_business.summary,
                        'created_by': new_business.created_by
                    }
                })
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
            404:
                description: Business is not registered
                schema:
                    properties:
                        response_message:
                            type: string
            401:
                description: Permission required
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
                    'message': 'Business successfuly deleted!',
                    'status_code': 204,
                    'data': {
                        'id': business.id,
                        'name': business.name,
                        'category': business.category,
                        'location': business.location,
                        'summary': business.summary,
                        'created_by': business.created_by
                    }
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
            500:
                description: Internal server error
                schema:
                    properties:
                        response_message:
                            type: string
        """
        user = User.query.filter_by(id=user_id).first()
        if user:
            business = Business.query.filter_by(created_by=user_id).first()
            if business:
                try:
                    business_object = jsonify({
                        'id': business.id,
                        'name': business.name,
                        'category': business.category,
                        'location': business.location,
                        'summary': business.summary,
                        'created_by': user.username
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
                    'response_message': 'You have not registered a business!',
                    'status_code': 204
                })
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
            -   in: query
                name: start
                description: pagination starting number
                required: true
                schema:
                    type: integer
            -   in: query
                name: limit
                description: pagination ending number
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
            200:
                description: A list of dictionaries of businesses
                schema:
                    name: business_list
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
                            type: integer
                            description: describes the id of the business owner
            404:
                description: Business not found
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

        user_request = request.args.get('q').lower()
        result_start = int(request.args.get('start'))
        result_limit = int(request.args.get('limit'))
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

                pagination_res = get_paginated_list(business_list,
                                                    '/api/v1/business/search',
                                                    result_start, result_limit)
                response = jsonify(pagination_res)
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
