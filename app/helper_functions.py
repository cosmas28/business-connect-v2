"""Create helper functions to be used in views module."""

import re

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

    if password.isalpha():
        response_message = {
            'message': 'Password must contain different characters!',
            'status_code': 406}
        return response_message
    if not password.isalnum():
        response_message = {
            'message': 'Password must contain alphanumeric characters!',
            'status_code': 406}
        return response_message
    if password.islower():
        response_message = {
            'message': 'Password must contain at least one capital character!',
            'status_code': 406}
        return response_message
    if password.isspace():
        response_message = {
            'message': 'Password must contain at least 6 characters!',
            'status_code': 406}
        return response_message
    if password.isdigit():
        response_message = {
            'message': 'Password must contain at least one alphabetical \
                         characters!',
            'status_code': 406}
        return response_message
    if len(password) <= 6:
        response_message = {
            'message': 'Password must be more than 6 characters!'}
        return response_message
    if password not in confirm_password:
        response_message = {
            'message': 'Password does not match the confirmation password!'}
        return response_message


def valid_email(email):
    valid = False
    match_email = re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*$)", email)
    if match_email:
        valid = True
    return valid


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
    """Check whether the business is already registered.

    Args:
        business_list(list): a list of business recodes.
        url(str): API endpoint url
        start(int): beginning index of a list
        limit(int): ending index of a list

    Returns:
        A dictionary of business records.
    """
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
        _object['previous'] = \
            url + '?start=%d&limit=%d' % (start_copy, limit_copy)

    if start + limit > count:
        _object['next'] = ''
    else:
        start_copy = start + limit
        _object['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    _object['business_list'] = business_list[(start - 1):(start - 1 + limit)]

    return _object
