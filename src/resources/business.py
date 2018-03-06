from flask import jsonify, Blueprint

from flask.ext.restful import (Resource, Api, reqparse)

from src.models.business import Business


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


business_api = Blueprint('resources.business', __name__)
api = Api(business_api)
api.add_resource(
    BusinessRecord,
    '/business',
    endpoint='business'
)