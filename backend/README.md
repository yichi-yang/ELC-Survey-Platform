# Backend API

## Set Up Development Environment

0. Django 4.0 supports Python 3.8, 3.9, and 3.10, so make sure you have one of
    the supported versions installed. You can install Python with your favorite
    package manager or [download an installer here](https://www.python.org/).
    The following steps assume you have Python 3.9 installed, but should also
    work for Python 3.8 and 3.10, just replace the numbers when applicable.

1. Clone the repo if you haven't already. Then go to this directory.

    ``` bash
    git clone git@github.com:yichi-yang/ELC-Survey-Platform.git
    cd ELC-Survey-Platform/backend
    git checkout develop
    ```

2. Set up a virtual environment so that we don't mess up the environment. Note
    depending on your Python installation you may need to use `python3`,
    `python3.9` or `py -3.9` instead of `python`.

    ``` bash
    python -m venv venv
    ```

3. Activate the virtual environment. This sets a few environment variables so
    `python` and `pip` points to the right version of binary
    [among other things](https://docs.python.org/3/library/venv.html)
    (You need to do this every time you restart your terminal).

    ``` bash
    source venv/bin/activate

    # or on Windows
    venv\Scripts\activate.bat

    # make sure you have the right version of Python
    python --version
    # Python 3.9.1
    ```

4. Install the required packages.

    ``` bash
    pip install -r requirements.txt
    ```

5. Run database migrations to set up the database. You'll need to do this again
    if the models change in the future (read more about migrations
    [here](https://docs.djangoproject.com/zh-hans/4.0/topics/migrations/))

    ``` bash
    python manage.py migrate
    ```

6. Now you can run the unit tests to make sure things are set up correctly.

    ``` bash
    python manage.py test
    ```

7. Now create a Django superuser that you'll use to log into the admin panel.

    ``` bash
    python manage.py createsuperuser
    # Then follow the instructions
    ```

8. Now let's start the builtin dev server to play with the backend.

    ``` bash
    python manage.py runserver
    ```

9. After you run the dev server, you can checkout the admin panel
    [127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and the browsable API
    [127.0.0.1:8000/api/](http://127.0.0.1:8000/api/). Log in with the superuser
    account you created in previous step. You can now try
    create/retrieve/update/delete surveys using the browsable API. If you modify
    the backend code, the dev server should automatically perform a hot reload
    to reflect the changes.

# API Documentation

## Authentication
* Login: `POST /api/auth/login/`
* Token Refresh: `POST /api/auth/token/refresh/`

## Surveys
* Create Survey : `POST /api/surveys/`
* List Survey : `GET /api/surveys/`
* Fetch Survey : `GET /api/surveys/<survey_id>/`
* Edit Survey (Partial Update): `PATCH /api/surveys/<survey_id>/`
* Edit Survey (Full Update) : `PUT /api/surveys/<survey_id>/`
* Delete Survey : `DELETE /api/surveys/<survey_id>/`
* Duplicate Survey : `POST /api/surveys/<survey_id>/duplicate/`

## Sessions
* Create Session : `POST /api/sessions/`
* List Sessions : `Get /api/sessions/`
* Fetch Session : `Get /api/sessions/<session_id>/`
* Delete Session : `DELETE /api/sessions/<session_id>`

## Codes
* Fetch Code : `GET /api/codes/<code>`