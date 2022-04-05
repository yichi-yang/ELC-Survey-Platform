# Deploying ELC Form

## Backend

In this section, we will deploy the backed on a Ubuntu 20.04 server. We will
use Gunicorn 'Green Unicorn' as the application server for our backend.
Other combinations of OS and software may also work, but that is outside the
scope of this guide. We assume at this point you already have a working server
and a domain that resolves to this server.

### Dependencies

0. Django 4.0 supports Python 3.8, 3.9, and 3.10, so make sure you have one of
    the supported versions installed. The following steps assume you have
    Python 3.8 installed (since it's shipped with Ubuntu 20.04), but should also
    work for Python 3.9 and 3.10, just replace the numbers when applicable.

1. Clone the repo if you haven't already. Then go to this directory. Note since
    the backend code contains sensitive information, the source code should not
    be placed in the root directory of the web server (e.g. `/var/www/html`).
    We recommend placing the files in `/opt/`. Here we assume you are logged in
    as `<user>` in group `<group>`. You should use a non-root userwith `sudo`
    access.

    ``` bash
    cd /opt

    # create a directory owned by you so you don't need to sudo when cloning
    sudo mkdir ELC-Survey-Platform && sudo chown <user>:<group> ELC-Survey-Platform

    # clone the repo (we actually only need /backend)
    git clone https://github.com/yichi-yang/ELC-Survey-Platform.git ELC-Survey-Platform
    
    cd ELC-Survey-Platform/backend

    # you should be on develop by default
    git checkout develop
    ```

2. Set up a virtual environment so that we don't mess up the environment.

    ``` bash
    #  On Debian/Ubuntu systems, you need to install the python3-venv using apt
    sudo apt update && sudo apt install python3.8-venv

    # create a virtual environment
    python3 -m venv venv
    ```

3. Activate the virtual environment. This sets a few environment variables so
    `python` and `pip` points to the right version of binary
    [among other things](https://docs.python.org/3/library/venv.html)
    (You need to do this every time you restart your terminal).

    ``` bash
    source venv/bin/activate

    # make sure you have the right version of Python
    python --version
    # Python 3.8.10
    ```

4. Install the required packages.

    ``` bash
    pip install -r requirements.deploy.txt
    ```

### Backend Configuration

Now we need to edit the settings file based on your deployment environment.
Open `elcform/settings.py` with your favorite text editor. There are several
things that we need to change. Note they are marked with `TODO:` so you can
just search for those.

1. Change `SECRET_KEY` to a unique, unpredictable value.
  [[?]](https://docs.djangoproject.com/en/4.0/ref/settings/#secret-key)

2. Change `HASHID_FIELD_SALT` to a long and secure salt value that is not
  the same as `SECRET_KEY`.
  [[?]](https://github.com/nshafer/django-hashid-field#installation)

3. You need to change `DEBUG = True` to `DEBUG = False`.
  [[?]](https://docs.djangoproject.com/en/4.0/ref/settings/#debug)

4. You need to put your domain name in `ALLOWED_HOSTS`,
  e.g. `ALLOWED_HOSTS=['example.com']`. This protects the
  API from HTTP Host header attacks. If you want the backend API to be
  accessible by IP addresses for debugging purposes, also put them
  in `ALLOWED_HOSTS`, e.g. `ALLOWED_HOSTS=['example.com', '203.0.113.1']`.
  [[?]](https://docs.djangoproject.com/en/4.0/ref/settings/#allowed-hosts)

5. Configure the **default** database in `DATABASES` to use your production
  database. Refer to [Django documentation](https://docs.djangoproject.com/en/4.0/ref/settings/#databases)
  for how to configure postgresql, mysql, etc. backends.

6. Leave `SECURE_HSTS_SECONDS` commented out for now.
  [[?]](https://docs.djangoproject.com/en/4.0/ref/settings/#secure-hsts-seconds)

7. Leave `STATIC_ROOT` commented out for now.
  [[?]](https://docs.djangoproject.com/en/4.0/ref/settings/#static-root)

Note this is the minimal configuration necessary to get the backend running.
For a complete list of setting, see
[Django documentation](https://docs.djangoproject.com/en/4.0/ref/settings/).

Use `python manage.py check --deploy` to check your configuration.
You **should not** see any warnings other than `security.W004` and
`security.W008`. We can ignore `security.W008` since we will set up our
webserver later to do ssl termination. We will come back to `security.W004`
later.

``` bash
python manage.py check --deploy

# ?: (security.W004) ...
# ?: (security.W008) ...
```

### Database Migration

Run database migrations to set up the database (read more about migrations
[here](https://docs.djangoproject.com/zh-hans/4.0/topics/migrations/)).

``` bash
python manage.py migrate

# You should see a list of 'Applying <something>... OK'
```

### Setting Up Gunicorn

1. Now you can use Gunicorn to serve the backend application and see if it works.

    ``` bash
    gunicorn elcform.wsgi
    ```

    You can use `curl` to see if the API works in a separate terminal.

    ``` bash
    curl localhost:8000/api/

    # {"surveys":"http://localhost:8000/api/surveys/", ...
    ```

    Note for this to work you need `'localhost'` in your `ALLOWED_HOSTS`.
    Otherwise it will return `'Bad Request (400)'`.

    By default Gunicorn listens on the loopback interface only. To make it listen
    on all interfaces so you can access the backend API from your browser,
    use `gunicorn elcform.wsgi -b 0.0.0.0:8080`. If you open
    `http://example.com:8000/api/` (replace with your domain) in your browser, you
    should see 'Api Root', but the page looks broken since static files
    (\*.js, \*.css, etc.) are not served. We will set up a web server to serve
    those later.

2. After you confirm Gunicorn works, we need to set up systemd to manage it.
    But before that, we will create a user specifically to run the backend.
    This allows us to easily set permissions for our backend service.

    ``` bash
    # add a new system user
    sudo useradd --system --no-create-home elcform
    
    # make the new user owner of /opt/ELC-Survey-Platform
    sudo chown -R elcform:elcform /opt/ELC-Survey-Platform

    # only elcform (or users in group elcform)
    # can access /opt/ELC-Survey-Platform
    # this protects the sensitive information e.g. SECRET_KEY
    sudo chmod -R u+rwX,g+rwX,o-rwx /opt/ELC-Survey-Platform

    # add yourself into the elcform group so you have rwx permission
    sudo usermod -aG elcform <user>

    # you need to log out and log in again for this to take effect
    ```

3. Now we create systemd unit files for our Gunicorn / backend service.

    Create the following unit files.

    `/etc/systemd/system/gunicorn.service`

    ``` ini
    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target

    [Service]
    Type=notify
    # the specific user that our service will run as
    User=elcform
    Group=elcform
    # another option for an even more restricted service is
    # DynamicUser=yes
    # see http://0pointer.net/blog/dynamic-users-with-systemd.html
    RuntimeDirectory=gunicorn
    WorkingDirectory=/opt/ELC-Survey-Platform/backend
    ExecStart=/opt/ELC-Survey-Platform/backend/venv/bin/gunicorn elcform.wsgi
    ExecReload=/bin/kill -s HUP $MAINPID
    KillMode=mixed
    TimeoutStopSec=5
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target
    ```

    `/etc/systemd/system/gunicorn.service`

    ``` ini
    [Unit]
    Description=gunicorn socket

    [Socket]
    ListenStream=/run/gunicorn.sock
    # Our service won't need permissions for the socket, since it
    # inherits the file descriptor by socket activation
    # only the nginx daemon will need access to the socket
    SocketUser=www-data
    # Optionally restrict the socket permissions even more.
    # SocketMode=600

    [Install]
    WantedBy=sockets.target
    ```

    This instructs systemd to listen on UNIX socket `/run/gunicorn.sock` and
    start gunicorn automatically in response to traffic.

    Note systemd wil be running Gunicorn with the new user we created. If you
    put ELC-Survey-Platform or the virtual environment in a different path,
    you need to edit `ExecStart` and `WorkingDirectory` accordingly.

4. Next enable and start the socket (it will autostart at boot too):

    ``` bash
    sudo systemctl enable --now gunicorn.socket
    ```

5. Once again, you can use curl to verify that `www-data` user can connect to
    that socket.

    ``` bash
    sudo -u www-data curl --unix-socket /run/gunicorn.sock http://localhost/api/

    # {"surveys":"http://localhost/api/surveys/", ...
    ```

6. You can check the status of the service and it should be running now.

    ``` bash
    sudo systemctl status gunicorn
    
    # ● gunicorn.service - gunicorn daemon
    #     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
    #     Active: active (running) since Mon 2022-04-04 04:12:17 UTC; 3min 44s ago
    # TriggeredBy: ● gunicorn.socket
    # Main PID: 15933 (gunicorn)
    # ...
    ```

    You can also view its logs.

    ``` bash
    sudo journalctl -u gunicorn
    ```

    > Note: Some how log files seemed to be broken when I tested this out.
    > `sudo journalctl` just returned 'No journal files were found.'
    > You can fix this by restarting journald `sudo systemctl restart systemd-journald`.
    > After that if you restart the gunicorn service you should see its logs.

### Setting Up Webserver

We will set up a webserver to:

1. Serve static files (\*.js, \*.css, etc.) including the fronted files
2. Proxy API requests to Gunicorn
3. SSL termination

We will use Caddy in this section since it's easy to set up. You can use
any webserver you like, such as Nginx or Apache HTTP Server, but configuring
those webserver is outside the scope of this guide.

1. First we need to install Caddy.

    ``` bash
    sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo tee /etc/apt/trusted.gpg.d/caddy-stable.asc
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
    sudo apt update
    sudo apt install caddy
    ```

    Now navigating to your domain in a browser should show Caddy's welcome page.

2. We will edit the Caddyfile at `/etc/caddy/Caddyfile` to make it serve our
    application.

    `/etc/caddy/Caddyfile`

    ``` text
    (django) {
        # Proxy to our django app (gunicorn)
        reverse_proxy unix//run/gunicorn.sock
    }

    example.com {

        handle /api/* {
            import django
        }

        handle /django-admin/* {
            import django
        }

        # static file
        handle {
            # Set this path to your site's directory.
            root * /var/www/html

            # see if the requested file exists server-side
            try_files {path} /index.html

            # Enable the static file server.
            file_server
        }
    }

    # Refer to the Caddy docs for more information:
    # https://caddyserver.com/docs/caddyfile
    ```

    Note you need to replace `example.com` with your domain.

    If you are using a webserver other than Caddy, you need to:

    1. For `/api/*` and `/django-admin/*` run a reverse proxy to the UNIX
        socket that Gunicorn is listening on (`/run/gunicorn.sock`).
    2. For the rest, serve from some directory containing static files
        (e.g. `/var/www/html`). The webserver should first check to see
        if a matching file exists. If so, it should serve that file; if not
        it should serve index.html. This allows the frontend (single page app)
        to handle routing internally.
    3. Set up SSL termination. The webserver should listen for https traffic on
        port 443, and redirect all http traffic to port 443. It should have a
        valid certificate (you can use letsencrypt).

    > :warning: **Warning**:
    > Caddy automatically gets certificates from letsencrypt and configures
    > https for you if you have a public domain, set up DNS correctly, and
    > [satisfy some other conditions](https://caddyserver.com/docs/automatic-https)
    > That's why SSL termination is not reflected in the above Caddyfile.
    > If you use a webserver other than Caddy, you **MUST** properly set up
    > SSL termination to make sure traffic is encrypted. Otherwise, passwords
    > will be sent in clear text.

3. Now the configuration.

    ``` bash
    sudo systemctl reload caddy
    ```

4. Now if you go to `https://example.com/api/` (replace with your domain) you
    should once again see 'Api Root'. It still looks broken but we will fix that
    next. Make sure that https works correctly.

5. Pick a directory to serve static files from. We recommend `/var/www/html`.
    Edit the backend configuration file `elcform/settings.py` and set
    `STATIC_ROOT` to `django-static` in that directory,
    e.g. `STATIC_ROOT = '/var/www/html/django-static'`.
    [[?]](https://docs.djangoproject.com/en/4.0/ref/settings/#static-root)

6. Use `python manage.py collectstatic` to copy all the static files for the
    backend to `STATIC_ROOT`.

    ``` bash
    sudo ./venv/bin/python manage.py collectstatic

    # ... static files copied to '/var/www/html/django-static'.

    # Now /var/www/html looks like this:
    # /var/www/html
    # └── django-static
    #     ├── admin
    #     ├── debug_toolbar
    #     └── rest_framework
    ```

    Now if you go to `https://example.com/api/` you should see the page properly
    styled.

## Frontend

After setting up the backend and the webserver, setting up the frontend is
relatively easy. All you need to do is to build the frontend and copy the
files into static file directory.

Note depending on the server configuration it might be faster (or easier if you
have node and npm installed) to build the frontend on you local machine.

1. Install nodejs and npm.

    ``` bash
    sudo apt update
    sudo apt install nodejs npm
    ```

2. Download dependencies.

    ``` bash
    cd /opt/ELC-Survey-Platform/frontend
    npm install
    ```

3. Build the frontend.

    ``` bash
    npm run build
    ```

4. Copy everything from `build` to the static file directory you picked earlier.

    ``` bash
    sudo cp -a build/. /var/www/html/

    # Now /var/www/html looks like this:
    # /var/www/html/
    # ├── asset-manifest.json
    # ├── django-static
    # │   ├── admin
    # │   ├── debug_toolbar
    # │   └── rest_framework
    # ├── favicon.ico
    # ├── index.html
    # ├── logo192.png
    # ├── logo512.png
    # ├── manifest.json
    # ├── robots.txt
    # └── static
    #     ├── css
    #     └── js
    ```

5. Now if you go to `https://example.com/` (replace with your domain) you should
    see the frontend working.

## Wrapping Up

### Following Best Practices

This guide only outlines the bear minimum to get the app working. You should
always follow the best practices to minimize security risks. For example, you
may want to enable firewall for the server (but of course leave port 80 and 443
open).

### HTTP Strict Transport Security

After you verify everything works, go back to `settings.py` and consider
uncommenting `SECURE_HSTS_SECONDS`. This instruct modern browsers to refuse to
connect to your domain name via an insecure connection.
[[?]](https://docs.djangoproject.com/en/4.0/ref/settings/#secure-hsts-seconds)

Read more about HSTS [here](https://docs.djangoproject.com/en/4.0/ref/middleware/#http-strict-transport-security).
Remember setting up HSTS incorrectly can break your site permanently.