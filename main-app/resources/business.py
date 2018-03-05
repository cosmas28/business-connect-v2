from flask import jsonify

from flask.ext.restful import Resource

from models.business import Business


class BusinessResource(Resource):
    