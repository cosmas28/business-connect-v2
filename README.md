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

* cd business-connect-v1/designs/UI
* Run index.html in your browser
* you can also view the page using this link [WeConnect](https://cosmas28.github.io/business-connect-v1/designs/UI/)

### API installation
To set up WeConnect API, make sure that you have python 3.6, postman and pip installed.

* Clone the Repo into your local directory.

```bash
$ git clone https://github.com/cosmas28/business-connect-v1.git
```

* create a virtual environment.

```bash
$ virtualenv <your_virtualenv>
```

* Activate your virtual environment

Navigate to the API directory.

```bash
$ cd business-connect-v1
$ git checkout challenge-two
```

To install the packages run pip install -r requirements.txt

## Usage

```bash
$ python app.py
```

Run the endpoints on Postman

## Test

Run the test using bash
```bash
$ pytest
```

Run the API endpoints using the following endpoints

POST `/api/v1/register` Register a user account
POST `/api/v1/login_user` log in users
POST `/api/v1/logout_user` logout users
POST `/api/v1/reset-password` Reset users passwords
POST `/api/v1/business` Registers business
GET `/api/v1/business` View all businesses
GET `/api/v1/businesses/<int:business_id>` view business by using business ID
DELETE `/api/v1/businesses/<int:business_id>` delete business by using business ID
PUT `/api/v1/businesses/<int:business_id>` update a registered business by using business ID
POST `/api/v1/businesses/<int:business_id>/reviews` add business review using business ID
GET `/api/v1/businesses/<int:business_id>/reviews` view business reviews using business ID

## Acknowledgements

* Andela Kenya Recruitment team for inspiration
