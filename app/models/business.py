"""Demonstrate all business functionalities.

This module provides methods that will enhance the business operations
such as business registration, business updates, deleting business and
view registered businesses.

"""


class Business(object):

    """Illustrate methods to manipulate business data.

    Attributes:
        business_records (dict): A dictionary that store the registered business records.

    """

    def __init__(self):
        self.business_records = {}

    def business_id_exist(self, business_id):
        business_id_existence = False

        if business_id in self.business_records:
            business_id_existence = True

        return business_id_existence

    def create_business(self, business_id, business_owner, business_name, business_location, business_category,
                        business_summary):
        """Register a new business.

        Args:
            business_id (int): business id parameter should be unique to identify each business.
            business_owner (str): business owner name parameter describes the business owner.
            business_name (str): business name that summarises what the business is.
            business_location (str): business location parameter describes the where the business is located.
            business_category (str): business category to group the business with the same features.
            business_summary (str): summary of what the business is about.

        Returns:
            A list of values of the registered business.

        Raises:
            KeyError: if the business id already exists.
            ValueError: if business id a negative number.

        """
        business_data = {
            'owner': business_owner,
            'name': business_name,
            'location': business_location,
            'category': business_category,
            'summary': business_summary
        }
        success_message = ''
        result_list = []

        if type(business_id) != int:
            raise TypeError('The business id must be an number!')
        elif business_id < 0:
            raise ValueError('The business id must be a positive number')
        elif self.business_id_exist(business_id):
            raise KeyError('The business id already exists')
        else:
            self.business_records[business_id] = business_data

        if business_id in self.business_records:
            success_message += 'The business is successfully registered!!!'

        single_record = self.business_records[business_id]

        for key in single_record:
            result_list.append(single_record[key])

        return {'value_list': result_list, 'message': success_message}

    def view_all_businesses(self):
        """View all registered businesses.

        Returns:
            A a dictionary of the registered businesses.

        """
        if len(self.business_records) == 0:
            return 'There is no registered business!'
        else:
            return self.business_records

    def view_business_by_id(self, business_id):
        """View a registered businesses using an id.

        Returns:
           A a dictionary of the registered businesses.

        """
        result_message = ''
        if business_id not in self.business_records:
            result_message += 'Business does not exist'
            raise KeyError('Key does not exist')

        if len(result_message) > 0:
            return {'message': result_message}
        elif len(result_message) == 0:
            single_record = self.business_records[business_id]
            return single_record

    def delete_business(self, business_id):
        """Delete a business.

        Args:
            business_id (int): business id parameter should be unique to identify each business.

        Returns:
           A successful message when the business record is deleted.

        """
        response = ''
        if len(str(business_id)) == 0:
            response += 'Business is required!'
        elif type(business_id) != int:
            response += 'The business id must be an number!'
            raise TypeError('The business id must be an number!')
        elif business_id < 0:
            response += 'The business id must be a positive number'
            raise ValueError('The business id must be a positive number')
        elif business_id not in self.business_records:
            response += 'Business does not exist'
            raise KeyError('Key does not exist')
        else:
            del self.business_records[business_id]
            response += 'Business deleted successfully!'

        return response

    def update_business(self, business_id, business_owner, business_name, business_location, business_category,
                        business_summary):
        """Update a registered business.

        Args:
            business_id (int): business id parameter should be unique to identify each business.
            business_owner (str): business owner name parameter describes the business owner.
            business_name (str): business name that summarises what the business is.
            business_location (str): business location parameter describes the where the business is located.
            business_category (str): business category to group the business with the same features.
            business_summary (str): summary of what the business is about.

        Returns:
            A list of values of the registered business.
            Success message

        Raises:
            KeyError: if the business id already exists.
            TypeError: if the business is not integer.
            ValueError: if business id a negative number.

        """
        response = ''

        if len(str(business_id)) == 0:
            response += 'Business id is required!'
        elif type(business_id) != int:
            raise TypeError('The business id must be an number!')
        elif business_id < 0:
            raise ValueError('The business id must be a positive number')
        elif business_id not in self.business_records:
            response += 'Business does not exist'
            raise KeyError('Key does not exist')
        else:
            business_record = self.business_records[business_id]
            business_record['owner'] = business_owner
            business_record['name'] = business_name
            business_record['category'] = business_category
            business_record['location'] = business_location
            business_record['summary'] = business_summary
            response += 'Business was successfully updated!'

        return response
