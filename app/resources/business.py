"""Demonstrate all business related API endpoints.

This module provides API endpoints to register business, view a single business, view all
businesses.

"""

from flask import Blueprint, request, make_response, jsonify

from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.models import Business
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

        Returns:
            A success message to indicate successful registration.

        Raises:
            Error message when business name is empty.
            Error message when business category is empty.
            Error message when business location is empty.
            Error message when business summary is empty.
            Error message when business name is already registered.

        """
        req_data = request.get_json(force=True)
        business_name = req_data['name']
        business_category = req_data['category']
        business_location = req_data['location']
        business_summary = req_data['summary']
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

        Returns:
            A json format records of the registered businesses.

        """

        try:
            businesses = Business.query.all()
            business_result = []

            for business in businesses:
                _object = {
                    'id': business.bid,
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
        """View a registered business by id.

        Returns:
            A json record of the registered business.

        """
        try:
            business = Business.query.filter_by(bid=business_id).first()
            if business is None:
                response = {
                    'response_message': 'Business id is not registered!'
                }
                return make_response(jsonify(response))
            else:
                business_object= {
                    'id': business.bid,
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
        """Update a registered businesses.

        Args:
            business_id (int): business id parameter should be unique to identify each business.

        Returns:
           A json object of the updated business.

        """

        req_data = request.get_json(force=True)
        business_name = req_data['name']
        business_category = req_data['category']
        business_location = req_data['location']
        business_summary = req_data['summary']

        try:
            current_business = Business.query.filter_by(bid=business_id).first()

            if current_business is None:
                response = {
                    'response_message': 'Business id is not registered!'
                }
                return make_response(jsonify(response))
            else:
                update_business = Business.query.filter_by(bid=business_id).update(dict(
                    name=business_name,
                    category=business_category,
                    location=business_location,
                    summary=business_summary
                ))
                db.session.commit()

                new_business = Business.query.filter_by(bid=business_id).first()
                business_object = {
                    'id': new_business.bid,
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
        """Delete a registered businesses.

        Args:
            business_id (int): business id parameter should be unique to identify each business.

        Returns:
           A successful message when the business record is deleted.

        """

        created_by = get_jwt_identity()
        try:
            business = Business.query.filter_by(bid=business_id).first()

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
    def get(self, business_category):
        """View registered businesses based on category.

        Returns:
            A json record of the registered business.

        """
        try:
            businesses = Business.query.filter_by(category=business_category).all()
            if businesses is None:
                response = {
                    'response_message': 'Businesses not found!'
                }
                return make_response(jsonify(response))
            else:
                business_result = []

                for business in businesses:
                    _object = {
                        'id': business.bid,
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


class BusinessLocation(Resource):

    """Illustrate API endpoints to view businesses in the same location."""

    @jwt_required
    def get(self):
        """View a registered business based in the same location.

        Returns:
            A json record of the registered business.

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
                        'id': business.bid,
                        'name': business.name,
                        'category': business.category,
                        'location': business.location,
                        'summary': business.summary,
                        'created_by': business.created_by
                    }
                    business_list.append(_object)

                # return make_response(jsonify(business_list=business_result))
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

        Returns:
            A json record of the registered business.

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
                        'id': business.bid,
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


business_api = Blueprint('resources.business', __name__)
api = Api(business_api)
api.add_resource(
    Businesses,
    '/businesses',
    endpoint='businesses'
)
api.add_resource(
    SingleBusiness,
    '/business/<int:business_id>',
    endpoint='business'
)
api.add_resource(
    BusinessCategory,
    '/business/category/<business_category>',
    endpoint='category'
)
api.add_resource(
    BusinessLocation,
    '/business/location',
    endpoint='location'
)
api.add_resource(
    SearchBusiness,
    '/business/search',
    endpoint='search'
)

