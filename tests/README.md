## Example Project for sockpuppet

This example is provided as a convenience feature to allow potential users to try the app straight from the app repo without having to create a django project.

It can also be used to develop the app in place.

To run this example, follow these instructions:

1. Install the requirements for the package (e.g. in a virtualenv):

		pip install -r requirements.txt

2. Make and apply migrations

		python manage.py makemigrations
		python manage.py migrate

3. In another terminal, install the needed Javascript packages and run the server

		npm install
		npm run build:watch

4. Back in your python virtualenv terminal, run the Django server

		python manage.py runserver

5. Access from the browser at `http://127.0.0.1:8000`

## Test suite

To run the test suite, call

		python manage.py test

You can also use pytest:

		pip install pytest pytest-django
		pytest
