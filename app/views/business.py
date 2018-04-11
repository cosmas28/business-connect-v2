"""Demonstrate all business related API endpoints.

This module provides API endpoints to register business, view a single business, view all
businesses.

"""

from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api

from app.models import Business
from app.models import db


def business_name_registered(name):
    """Check whether the business is already registered.

    Args:
        name(str): Unique business name.

    Returns:
        Boolean value.
    """

    registered = Business.query.filter_by(name=name).first()

    if registered:
        return True


class Businesses(Resource):

    """Illustrate API endpoints to register and view businesses."""

    @jwt_required
    def post(self):
        """Register a business.
        ---
        tags:
            -   businesses
        parameters:
            -   in: body
                name: body
                schema:
                    $ref: '#/definitions/User'
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            201:
                description: Business has been registered successfully!
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                response_message:
                                    type: string
                                    description: message to show successful business registration
                                status_code:
                                    type: integer
                                    description: HTTP status code
        """
        req_data = request.get_json(force=True)
        business_name = req_data.get('name')
        business_category = req_data.get('category')
        business_location = req_data.get('location')
        business_summary = req_data.get('summary')
        created_by = get_jwt_identity()

        try:

            if len(business_name) == 0:
                response = {
                    'response_message': 'Business name is required!'
                }
                return make_response(jsonify(response))
            elif len(business_category) == 0:
                response = {
                    'response_message': 'Business category is required!'
                }
                return make_response(jsonify(response))
            elif len(business_location) == 0:
                response = {
                    'response_message': 'Business location is required!'
                }
                return make_response(jsonify(response))
            elif len(business_summary) == 0:
                response = {
                    'response_message': 'Business summary is required!'
                }
                return make_response(jsonify(response))
            elif business_name_registered(business_name):
                response = {
                    'response_message': 'Business name already registered!'
                }
                return make_response(jsonify(response))
            else:
                business = Business(business_name, business_category, business_location, business_summary, created_by)
                db.session.add(business)
                db.session.commit()

                response = {
                    'response_message': 'Business has been registered successfully!',
                    'status_code': 201
                }

                return make_response(jsonify(response))

        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))

    @jwt_required
    def get(self):
        """View all registered businesses.
        ---
        tags:
            -   businesses
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schema/Business'
        components:
            schema:
                Business:
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
                            description: business category used to group businesses
                        location:
                            type: string
                            description: describes where the business is located
                        summary:
                            type: string
                            description: business description
                        created_by:
                            type: integer
                            description: describes the id of the business owner
            parameters:
                Path:
                    schema:
                        required: true
                        type: integer
                        description: a unique business id
            parameters:
                IntQueryString:
                    schema:
                        required: true
                        type: integer
                        description: numeric number to limit search results
            parameters:
                StrQueryString:
                    schema:
                        required: true
                        type: string
                        description: search criteria
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

            return make_response(jsonify(business_list=business_result))
        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))


class SingleBusiness(Resource):

    """Illustrate API endpoints to manipulate single business."""

    @jwt_required
    def get(self, business_id):
        """view a registered business by id.
        ---
        tags:
            -   businesses
        parameters:
            -   in: path
                name: business_id
                schema:
                    $ref: '#/components/parameters/Path'
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schema/Business'
        """
        try:
            business = Business.query.filter_by(id=business_id).first()
            if business is None:
                response = {
                    'response_message': 'Business id is not registered!'
                }
                return make_response(jsonify(response))
            else:
                business_object= {
                    'id': business.id,
                    'name': business.name,
                    'category': business.category,
                    'location': business.location,
                    'summary': business.summary,
                    'created_by': business.created_by
                }

                return make_response(jsonify(business_object))
        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))

    @jwt_required
    def put(self, business_id):
        """Update a registered business.
        ---
        tags:
            -   businesses
        parameters:
            -   in: path
                name: business_id
                schema:
                    $ref: '#/components/parameters/Path'
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schema/Business'
        """

        req_data = request.get_json(force=True)
        business_name = req_data.get('name')
        business_category = req_data.get('category')
        business_location = req_data.get('location')
        business_summary = req_data.get('summary')

        try:
            current_business = Business.query.filter_by(id=business_id).first()

            if current_business is None:
                response = {
                    'response_message': 'Business id is not registered!'
                }
                return make_response(jsonify(response))
            else:
                update_business = Business.query.filter_by(id=business_id).update(dict(
                    name=business_name,
                    category=business_category,
                    location=business_location,
                    summary=business_summary
                ))
                db.session.commit()

                new_business = Business.query.filter_by(id=business_id).first()
                business_object = {
                    'id': new_business.id,
                    'name': new_business.name,
                    'category': new_business.category,
                    'location': new_business.location,
                    'summary': new_business.summary,
                    'created_by': new_business.created_by
                }

                return make_response(jsonify(business_object))

        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))

    @jwt_required
    def delete(self, business_id):
        """Delete a registered business.
        ---
        tags:
            -   businesses
        parameters:
            -   in: path
                name: business_id
                schema:
                    $ref: '#/components/parameters/Path'
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            204:
                description: No Content
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                response_message:
                                    type: string
                                    description: successful delete message
        """

        created_by = get_jwt_identity()
        try:
            business = Business.query.filter_by(id=business_id).first()

            if business is None:
                response = {
                    'response_message': 'Business id is not registered!'
                }
                return make_response(jsonify(response))
            elif business.created_by != created_by:
                response = {
                    'response_message': 'Permission required to delete this business!'
                }
                return make_response(jsonify(response))
            else:
                db.session.delete(business)
                db.session.commit()
                response = {
                    'response_message': 'Business has been deleted successfully!'
                }

                return make_response(jsonify(response))
        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))


class BusinessCategory(Resource):

    """Illustrate API endpoints to view businesses with the same category."""

    @jwt_required
    def get(self):
        """View registered businesses based on category.
        ---
        tags:
            -   businesses
        parameters:
            -   in: query
                name: q
                schema:
                    $ref: '#/components/schema/StrQueryString'
            -   in: query
                name: start
                schema:
                    $ref: '#/components/schema/IntQueryString'
            -   in: query
                name: limit
                schema:
                    $ref: '#/components/schema/IntQueryString'
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schema/Business'
        """

        user_request = request.args.get('q')
        result_start = int(request.args.get('start'))
        result_limit = int(request.args.get('limit'))
        try:
            businesses = Business.query.filter_by(category=user_request).all()
            if businesses is None:
                response = {
                    'response_message': 'Businesses not found!'
                }
                return make_response(jsonify(response))
            else:
                business_list = []

                for business in businesses:
                    _object = {
                        'id': business.id,
                        'name': business.name,
                        'category': business.category,
                        'location': business.location,
                        'summary': business.summary,
                        'created_by': business.created_by
                    }
                    business_list.append(_object)

                pagination_res = get_paginated_list(business_list, '/api/v1/business/search',
                                                    result_start, result_limit)
                return make_response(jsonify(pagination_res))
        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))


class BusinessLocation(Resource):

    """Illustrate API endpoints to view businesses in the same location."""

    @jwt_required
    def get(self):
        """View registered businesses based on location.
        ---
        tags:
            -   businesses
        parameters:
            -   in: query
                name: q
                schema:
                    $ref: '#/components/schema/StrQueryString'
            -   in: query
                name: start
                schema:
                    $ref: '#/components/schema/IntQueryString'
            -   in: query
                name: limit
                schema:
                    $ref: '#/components/schema/IntQueryString'
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schema/Business'
        """

        user_request = request.args.get('q')
        result_start = int(request.args.get('start'))
        result_limit = int(request.args.get('limit'))
        try:
            businesses = Business.query.filter_by(location=user_request).all()
            if businesses is None:
                response = {
                    'response_message': 'Businesses not found!'
                }
                return make_response(jsonify(response))
            else:
                business_list = []

                for business in businesses:
                    _object = {
                        'id': business.id,
                        'name': business.name,
                        'category': business.category,
                        'location': business.location,
                        'summary': business.summary,
                        'created_by': business.created_by
                    }
                    business_list.append(_object)

                pagination_res = get_paginated_list(business_list, '/api/v1/business/search',
                                                    result_start, result_limit)
                return make_response(jsonify(pagination_res))
        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))


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
                name: q
                schema:
                    $ref: '#/components/schema/StrQueryString'
            -   in: query
                name: start
                schema:
                    $ref: '#/components/schema/IntQueryString'
            -   in: query
                name: limit
                schema:
                    $ref: '#/components/schema/IntQueryString'
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schema/Business'
        """

        user_request = request.args.get('q')
        result_start = int(request.args.get('start'))
        result_limit = int(request.args.get('limit'))
        try:
            businesses = Business.query.filter(Business.name.startswith(user_request)).all()
            if businesses is None:
                response = {
                    'response_message': 'Businesses not found!'
                }
                return make_response(jsonify(response))
            else:
                business_list = []

                for business in businesses:
                    _object = {
                        'id': business.id,
                        'name': business.name,
                        'category': business.category,
                        'location': business.location,
                        'summary': business.summary,
                        'created_by': business.created_by
                    }
                    business_list.append(_object)

                pagination_res = get_paginated_list(business_list, '/api/v1/business/search',
                                                    result_start, result_limit)
                return make_response(jsonify(pagination_res))
        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))


def get_paginated_list(business_list, url, start, limit):
    count = len(business_list)
    _object = {}
    _object['start'] = start
    _object['limit'] = limit
    _object['count'] = count

    if start == 1:
        _object['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        _object['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)

    if start + limit > count:
        _object['next'] = ''
    else:
        start_copy = start + limit
        _object['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    _object['business_list'] = business_list[(start - 1):(start - 1 + limit)]

    return _object


business_api = Blueprint('views.business', __name__)
api = Api(business_api)
api.add_resource(
    Businesses,
    '/businesses',
    endpoint='businesses'
)
api.add_resource(
    SingleBusiness,
    '/businesses/<int:business_id>',
    endpoint='business'
)
api.add_resource(
    BusinessCategory,
    '/businesses/category',
    endpoint='category'
)
api.add_resource(
    BusinessLocation,
    '/businesses/location',
    endpoint='location'
)
api.add_resource(
    SearchBusiness,
    '/businesses/search',
    endpoint='search'
)

