[![Build Status](https://travis-ci.org/cosmas28/business-connect-v2.svg?branch=develop)](https://travis-ci.org/cosmas28/business-connect-v2)
[![Coverage Status](https://coveralls.io/repos/github/cosmas28/business-connect-v2/badge.svg?branch=master)](https://coveralls.io/github/cosmas28/business-connect-v2?branch=master)
WeConnect provides a platform that brings businesses and individuals together.
This platform creates awareness for businesses and gives the users the ability
to write reviews about the businesses they have interacted with.

### API installation
To set up WeConnect API, make sure that you have python 3.6, postman and pip installed.

* Clone the Repo into your local directory.

```bash
$ git clone https://github.com/cosmas28/business-connect-v2.git
```

* create a virtual environment.

```bash
$ virtualenv <your_virtualenv>
```

* Activate your virtual environment

Navigate to the API directory.

```bash
$ cd business-connect-v2
```

To install the packages run pip install -r requirements.txt

## Database setup instructions

* Install PostgreSQL.
* Create a new database.
* Change Database configuration at `SQLALCHEMY_DATABASE_URI` environment variable to include your database name, password
    and user name i.e `SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@localhost/database_name'`

## How to make migrations

* Run migrations initialization using this command `$ python manage.py db init`
* Run actual migrations using `$ python manage.py db migrate`
* Finally apply migrations using `$ python manage.py db upgrade`
* Then each time the database models change repeat the migrate and upgrade commands.

## Usage

```bash
$ python manage.py runserver
```

## How to view API documentation

* Run the server `$ python manage.py runserver`
* Browse http://localhost:5000/apidocs/

Run the endpoints on Postman

## Test

Run the test using bash
```bash
$ pytest
```

Run the API endpoints using the following URLs

HTTP Method | URL | Functionality
----------- | --- | -------------
POST | /api/v2/auth/register | Creates a new user account
POST | /api/v2/auth/login | logs in a user
POST | /api/v2/auth/logout | logs in a user
POST | /api/v2/auth/reset-password | Password Reset
POST | /api/v2/businesses | Registers a business
GET | /api/v2/businesses | Retrieves all businesses
GET | /api/v2/businesses/<int:business_id> | get a business
DELETE | /api/v2/businesses/<int:business_id> | Remove a business
PUT | /api/v2/businesses/<int:business_id> | Update a business profile
POST | /api/v2/businesses/<int:business_id>/reviews | Add a review for a business
GET | /api/v2/businesses/<int:business_id>/reviews | Get all reviews for a business
GET | /api/v2/businesses/location?q=<location>&start=<start>&limit=<limit> | Filter businesses based on location
GET | /api/v2/businesses/location?q=<category>&start=<start>&limit=<limit> | Filter businesses based on category
GET | /api/v2/businesses/search?q=<business_name>&start=<start>&limit=<limit> | Search for a business

## Acknowledgements

* Andela Kenya Recruitment team for inspiration
