[![Build Status](https://travis-ci.org/cosmas28/business-connect-v1.svg?branch=challenge-two)](https://travis-ci.org/cosmas28/business-connect-v1)
[![Coverage Status](https://coveralls.io/repos/github/cosmas28/business-connect-v1/badge.svg?branch=masterchallenge-two)](https://coveralls.io/github/cosmas28/business-connect-v1?challenge-two)# business-connect-v1

WeConnect provides a platform that brings businesses and individuals together.
This platform creates awareness for businesses and gives the users the ability
to write reviews about the businesses they have interacted with.

## HTML templates installation

* Clone the master branch into your local directory.

```bash
$ git clone https://github.com/cosmas28/business-connect-v1.git
```

* cd business-connect-v2/designs/UI
* Run index.html in your browser
* you can also view the page using this link [WeConnect](https://cosmas28.github.io/business-connect-v1/designs/UI/)

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

## Usage

```bash
$ python run.py
```

Run the endpoints on Postman

## Test

Run the test using bash
```bash
$ pytest
```

Run the API endpoints using the following URLs

* POST `/api/v2/register` Register a user account
* POST `/api/v2/login_user` log in users
* POST `/api/v2/logout_user` logout users
* POST `/api/v2/reset-password` Reset users passwords
* POST `/api/v2/business` Registers business
* GET `/api/v2/business` View all businesses
* GET `/api/v2/businesses/<int:business_id>` view business by using business ID
* DELETE `/api/v2/businesses/<int:business_id>` delete business by using business ID
* PUT `/api/v2/businesses/<int:business_id>` update a registered business by using business ID
* POST `/api/v2/businesses/<int:business_id>/reviews` add business review using business ID
* GET `/api/v2/businesses/<int:business_id>/reviews` view business reviews using business ID
* GET `/api/v2/business/location?q=<business_location>&start=<starting_number>&limit=<number_of_results>`
 view businesses based on the same location
* GET `/api/v2/business/category?q=<business_category>&start=<starting_number>&limit=<number_of_results>`
view businesses on the same category
* GET `/api/v2/business/search?q=<business_name>&start=<starting_number>&limit=<number_of_results>`
 search a specified number of businesses

## Acknowledgements

* Andela Kenya Recruitment team for inspiration
