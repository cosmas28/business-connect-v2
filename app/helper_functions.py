"""Create helper functions to be used in views module."""

from app.models import User
from app.models import Business


def email_exist(email):
    """Check if user email is already registered."""

    user_email = User.query.filter_by(email=email).first()
    return user_email


def username_exist(user_name):
    """Check if username is already registered."""

    user_name = User.query.filter_by(username=user_name.lower()).first()
    return user_name


def valid_password(password, confirm_password):
    """Check whether the password have more than 6 characters."""

    if len(password) <= 6:
        response_message = {'message': 'Password must be more than 6 characters!'}
        return response_message
    if password not in confirm_password:
        response_message = {'message': 'Password does not match the confirmation password!'}
        return response_message


def business_name_registered(name):
    """Check whether the business is already registered.

    Args:
        name(str): Unique business name.

    Returns:
        Boolean value.
    """

    registered = Business.query.filter_by(name=name).first()
    return registered


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

