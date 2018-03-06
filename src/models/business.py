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

    def create_business(self, b_id, b_owner, b_name, b_location, b_category, b_summary):
        """Register a new business.

        Args:
            b_id (int): business id parameter should be unique to identify each business.
            b_owner (str): business owner name parameter describes the business owner.
            b_name (str): business name that summarises what the business is.
            b_location (str): business location parameter describes the where the business is located.
            b_category (str): business category to group the business with the same features.
            b_summary (str): summary of what the business is about.

        Returns:
            A list of values of the registered business.

        Raises:
            KeyError: if the business id already exists.
            ValueError: if business id a negative number.

        """
        user_data = {
            'owner': b_owner,
            'name': b_name,
            'location': b_location,
            'category': b_category,
            'summary': b_summary
        }
        success_message = ""
        result_list = []

        if type(b_id) != int:
            raise TypeError("The business id must be an number!")
        elif b_id < 0:
            raise ValueError("The business id must be a positive number")
        elif b_id in self.business_records:
            raise KeyError("The business id already exists")
        else:
            self.business_records[b_id] = user_data

        if b_id in self.business_records:
            success_message += "The business is successfully registered!!!"

        single_record = self.business_records[b_id]

        for key in single_record:
            result_list.append(single_record[key])

        return {"value_list": result_list, "message": success_message}

    def view_all_businesses(self):
        """View all registered businesses.

                Returns:
                    A a dictionary of the registered businesses.

                """
        if len(self.business_records) == 0:
            return "There is no registered business!"
        else:
            return self.business_records
