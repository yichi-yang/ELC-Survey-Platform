# Deploying ELC Form

## Backend

In this section, we will deploy the backed on a Ubuntu 20.04 server. We will
use Gunicorn 'Green Unicorn' as the application server for our backend.
Other combinations of OS and software may also work, but that is outside the
scope of this guide.

### Dependencies

0. Django 4.0 supports Python 3.8, 3.9, and 3.10, so make sure you have one of
    the supported versions installed. You can install Python with your favorite
    package manager or [download an installer here](https://www.python.org/).
    The following steps assume you have Python 3.9 installed, but should also
    work for Python 3.8 and 3.10, just replace the numbers when applicable.

1. Clone the repo if you haven't already. Then go to this directory. Note since
    the backend code contains sensitive information, the source code should not
    be placed in the root directory of the web server (e.g. `/var/www/html`).
    We recommend placing the files in `/opt/`.

    ``` bash
    cd /opt

    # create a directory owned by you so you don't need to sudo when cloning
    sudo mkdir ELC-Survey-Platform && chown <user>:<group> ELC-Survey-Platform

    # clone the repo (we actually only need /backend)
    git clone https://github.com/yichi-yang/ELC-Survey-Platform.git ELC-Survey-Platform
    
    cd ELC-Survey-Platform/backend

    # you should be on develop by default
    git checkout develop
    ```

2. Set up a virtual environment so that we don't mess up the environment.

    ``` bash
    python3 -m venv venv
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