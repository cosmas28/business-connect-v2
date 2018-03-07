from flask import jsonify, json, Blueprint, abort, request

from flask.ext.restful import (Resource, Api, reqparse, fields, marshal)

from src.models.business import Business

business_info = {}
business_info['id'] = {}
business_info['id']['owner'] = fields.String
business_info['id']['name'] = fields.String
business_info['id']['category'] = fields.String
business_info['id']['location'] = fields.String
business_info['id']['summary'] = fields.String

business_fields = {
    'owner': fields.String,
    'name': fields.String,
    'category': fields.String,
    'location': fields.String,
    'summary': fields.String
}

business = Business()

class BusinessRecord(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('business_id',
                                   required=True,
                                   help='Business id is required',
                                   location=['form', 'json']
                                    )
        self.reqparse.add_argument('business_owner',
                                   required=True,
                                   help='Business owner is required',
                                   location=['form', 'json'])
        self.reqparse.add_argument('business_name',
                                   required=True,
                                   help='Business name is required',
                                   location=['form', 'json'])
        self.reqparse.add_argument('business_category',
                                   required=True,
                                   help='Business category is required',
                                   location=['form', 'json'])
        self.reqparse.add_argument('business_location',
                                   required=True,
                                   help='Business location is required',
                                   location=['form', 'json'])
        self.reqparse.add_argument('business_summary',
                                   required=True,
                                   help='Business summary is required',
                                   location=['form', 'json'])

    def post(self):
        req_data = request.get_json()
        business_id = req_data['business_id']
        business_owner = req_data['business_owner']
        business_name = req_data['business_name']
        business_category = req_data['business_category']
        business_location = req_data['business_location']
        business_summary = req_data['business_summary']

        save_result = business.create_business(business_id, business_owner, business_name, business_category,
                                               business_location, business_summary)
        return save_result["message"], 201

    def get(self):
        """View all registered businesses.

        Returns:
            A json records of the registered businesses.

        """

        business_dict = business.view_all_businesses()
        return json.dumps(marshal(business_dict, business_info)), 200


class OneBusinessRecord(Resource):

    """Illustrate API endpoints to manipulate business data.

       Attributes:
           business (class): A class that implement business related methods.

       """

    def get(self, business_id):
        """View a registered business by id.

        Returns:
            A json record of the registered business.

        """
        response = business.view_business_by_id(business_id)
        print("This is the response", response)

        if response.get("message") == "There is no registered business!":
            return "Business does not exist", abort(404)

        return marshal(response, business_fields), 200


business_api = Blueprint('resources.business', __name__)
api = Api(business_api)
api.add_resource(
    BusinessRecord,
    '/business',
    endpoint='business'
)
api.add_resource(
    OneBusinessRecord,
    '/businesses/<int:business_id>',
    endpoint='businesses'
)