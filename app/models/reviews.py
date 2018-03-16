"""Demonstrate all business reviews related methods.

This module provides methods that will enhance the business reviews operations
such as adding review and view reviews of a business.

"""

from app import business


class Reviews(object):

    """Illustrate methods to manipulate reviews data.

    Attributes:
        business_reviews (list): A list of dictionary that store the registered business reviews.

    """

    def __init__(self):
        self.business_reviews = []

    def add_review(self, business_id, review, created_at):
        """Register a new business.

        Args:
            business_id (int): business id parameter should be unique to identify each business.
            review (str): A description for a business review.
            created_at (str): A date showing when the review was posted.


        Returns:
            A successful message.

        Raises:
            KeyError: if the business id does not exists.
            ValueError: if business id is empty.
            ValueError: if review is empty.

        """

        review_data = {
            'business_id': business_id,
            'review': review,
            'created_at': created_at
        }
        response = ''

        if len(str(business_id)) == 0:
            response += 'Business id is required!'
        elif business_id not in business.business_records:
            response += 'Business id does not exist'
            raise KeyError('Business id does not exist')
        elif len(review) == 0:
            response += 'Business review was not provided!'
        else:
            self.business_reviews.append(review_data)
            response += 'Business review added successfully!'

        return response

    def view_business_reviews(self, business_id):
        """View a registered businesses using an id.

        Returns:
           A a dictionary of the registered businesses.

        """
        reviews = []

        if len(str(business_id)) == 0:
            return 'Business id is required!'
        elif business_id not in business.business_records:
            return 'Business ID does not exist!'
        else:
            for review in self.business_reviews:
                if review['business_id'] == business_id:
                    reviews.append({
                        'review': review['review'],
                        'created_at': review['created_at']
                    })

        return reviews
