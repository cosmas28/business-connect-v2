class Business:
    """Create business for registered users

    Args:
        b_owner: registered user who owns a business
        b_id: unique business number
        b_name: business name
        b_location: business location

    """
    def __init__(self, business_id, business_owner, business_name, business_location, business_category):
        self.b_id = business_id
        self.b_owner = business_owner
        self.b_name = business_name
        self.b_location = business_location
        self.b_category = business_category
        self.business_records = []

    def create_business(self):
        user_data = {
            'id': self.b_id,
            'owner': self.b_owner,
            'name': self.b_name,
            'location': self.b_location,
            'category': self.b_category
        }
        self.business_records.append(user_data)
        """
        if len(self.business_records) != 1:
            return False """
        if self.b_id != self.business_records[]
        return True