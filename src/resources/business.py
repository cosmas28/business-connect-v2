from flask import jsonify, json, Blueprint, abort

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
        business = Business()
        args = self.reqparse.parse_args()
        save_result = business.create_business(int(args['business_id']), args['business_owner'], args['business_name'],
                                               args['business_category'], args['business_location'], args['business_summary'])
        return save_result["message"], 201

    def get(self):
        """View all registered businesses.

        Returns:
            A json records of the registered businesses.

        """

        business = Business()
        business_dict = business.view_all_businesses()
        return json.dumps(marshal(business_dict, business_info)), 200


class OneBusinessRecord(Resource):

    """Illustrate API endpoints to manipulate business data.

       Attributes:
           business (class): A class that implement business related methods.

       """
    def __init__(self):
        self.business = Business()

    def get(self, business_id):
        """View a registered business by id.

        Returns:
            A json record of the registered business.

        """
        response = self.business.view_business_by_id(business_id)

        if response["message"] == "There is no registered business!":
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