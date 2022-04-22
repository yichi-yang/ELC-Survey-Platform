# Deploying ELC Form

> Note: We recommend following the guide in the exact order written.
> Some parts may not make sense if you skip over earlier sections and you will
> likely run into problems.

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

### Install Database Driver

Depending on the database you plan to use, you may need to install a matching
database driver. Please refer to the
[Django documentation](https://docs.djangoproject.com/en/4.0/ref/databases/)
and check if a database driver is required for your database.

For example, to connect to a MySQL database, you need to install `mysqlclient`.

``` bash
# if haven't activated your venv already
source venv/bin/activate

# install mysqlclient
pip install mysqlclient
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

5. You need to put `https://your-domain-name` in `CSRF_TRUSTED_ORIGINS`,
  e.g. `CSRF_TRUSTED_ORIGINS = ['https://example.com']`. This protects the
  API from cross-site request forgery attacks.
  [[?]](https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-trusted-origins)

6. Configure the **default** database in `DATABASES` to use your production
  database. Refer to [Django documentation](https://docs.djangoproject.com/en/4.0/ref/settings/#databases)
  for how to configure postgresql, mysql, etc. backends.

7. Leave `SECURE_HSTS_SECONDS` commented out for now.
  [[?]](https://docs.djangoproject.com/en/4.0/ref/settings/#secure-hsts-seconds)

8. Leave `STATIC_ROOT` commented out for now.
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
    use `gunicorn elcform.wsgi -b 0.0.0.0:8000`. If you open
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

    `/etc/systemd/system/gunicorn.socket`

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

1. For `/api/*` and `/django-admin/*` run a reverse proxy to the UNIX
    socket that Gunicorn is listening on (`/run/gunicorn.sock`).
2. For the rest, serve from some directory containing static files
    (e.g. `/var/www/html`). The webserver should first check to see
    if a matching file exists. If so, it should serve that file; if not
    it should serve index.html. This allows the frontend (single page app)
    to handle routing internally.
3. Set up SSL termination. The webserver should listen for https traffic on
    port 443, and redirect all http traffic to port 443. It should have a
    valid certificate (you can use, for example, letsencrypt).

The following subsections show you how to do the above 3 things with Caddy
or Nginx. You can use any webserver you like, but configuring those webserver
is outside the scope of this guide.

#### Caddy

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

            # See if the requested file exists server-side
            try_files {path} /index.html

            # Enable the static file server.
            file_server
        }
    }

    # Refer to the Caddy docs for more information:
    # https://caddyserver.com/docs/caddyfile
    ```

    Note you need to replace `example.com` with your domain.

    > :warning: **Warning**:
    > Caddy automatically gets certificates from letsencrypt and configures
    > https for you if you have a public domain, set up DNS correctly, and
    > [satisfy some other conditions](https://caddyserver.com/docs/automatic-https)
    > That's why SSL termination is not reflected in the above Caddyfile.
    > If you use a webserver other than Caddy, you **MUST** properly set up
    > SSL termination to make sure traffic is encrypted. Otherwise, passwords
    > will be sent in clear text.

3. Reload the configuration.

    ``` bash
    sudo systemctl reload caddy
    ```

4. Now if you go to `https://example.com/api/` (replace with your domain) you
    should see 'Api Root'. It still looks broken but we will fix that next.
    Make sure that https works correctly.

#### Nginx

1. Install Nginx (if it's not installed already).

    ``` bash
    sudo apt update
    sudo apt install nginx
    ```

    Now navigating to your domain in a browser should show Nginx's welcome page.

2. Add a new site configuration to `/etc/nginx/sites-available/`.

    `/etc/nginx/sites-available/elcform`

    ``` text
    server {
        listen 443 ssl;

        # You can use certbot to issue a certificate,
        # see https://certbot.eff.org/.
        ssl_certificate /path/to/certificate;
        ssl_certificate_key /path/to/certificate_key;

        server_name example.com;
        
        # static file
        location / {
            # Set this path to your site's directory.
            root /var/www/html;

            try_files $uri $uri/ /index.html;
        }

        # Proxy to our django app (gunicorn)
        location ~ ^/(api|django-admin)/ {
            proxy_set_header X-Forwarded-Host $host:$server_port;
            proxy_set_header X-Forwarded-Server $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_pass http://unix:/run/gunicorn.sock;
        }
    }

    # redirect http -> https
    server {
        listen 80;
        server_name example.com;
        return 301 https://$host$request_uri;
    }
    ```

    Note you need to replace `example.com` with your domain.

3. Enable your site (by making a symbolic link).

    ``` bash
    ln -s /etc/nginx/sites-available/elcform /etc/nginx/sites-enabled/elcform
    ```

4. Reload the configuration.

    ``` bash
    # test your config to make sure it's valid
    sudo nginx -t

    # reload Nginx
    sudo nginx -s reload
    ```

5. Now if you go to `https://example.com/api/` (replace with your domain) you
    should see 'Api Root'. It still looks broken but we will fix that next.
    Make sure that https works correctly.

### Collect Backend Static Files

Now we'll fix `https://example.com/api/` page by collecting backend static
files (css, js) into the *static file directory*. The *static file directory*
is the path after `root` in your Caddyfile or Nginx configuration
(`/var/www/html` in the above example).

1. Go back to `elcform/settings.py`, set `STATIC_ROOT` to `django-static`
    within the *static file directory*,
    e.g. `STATIC_ROOT = '/var/www/html/django-static'`.
    [[?]](https://docs.djangoproject.com/en/4.0/ref/settings/#static-root)

2. Use `python manage.py collectstatic` to copy all the static files for the
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
relatively easy. All you need to do is to copy the frontend static files into
the *static file directory*.

### Building the Frontend

You can either download a prebuilt version of the frontend or build from source.
If you don't need to change anything we recommend using the prebuilt version.

#### Using Prebuilt Frontend

We have the latest build of our frontend
[here](https://github.com/yichi-yang/ELC-Survey-Platform/releases/latest).
You can download the latest frontend build like this:

``` bash
# download the latest release
wget https://github.com/yichi-yang/ELC-Survey-Platform/releases/latest/download/frontend.zip

# create a directory to unzip into
mkdir build

# unzip the zip file
unzip frontend.zip -d build
```

#### Building From Source

> Note: Building the frontend requires > 1.8 GB of RAM. If your server has
> < 2 GB of RAM, building the frontend can lead to thrashing and take forever
> to finish. In this case you can build the frontend on your local machine and
> use scp or sftp to copy `build` to your server.

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

### Copy to the Static File Directory

Next, you need to copy the frontend build into the *static file directory*.

1. Copy everything from `build` to the *static file directory*.

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

2. Now if you go to `https://example.com/` (replace with your domain) you should
    see the frontend working.

## Security Considerations

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

## Updating ELC Form

If the frontend or the backend change in the future, you may want to deploy
a new version to your server. You can easily update them following these steps:

### Updating the Backend

> Note: You don't need to stop Gunicorn to update the backend.

1. Pull the updated codebase. Make sure `settings.py` is not overwritten.
    (you could `git stash` it and `git stash pop` after you pull the changes).

2. Run `python manage.py check --deploy` again to make sure your settings look
    good (see [Backend Configuration](#backend-configuration)).

3. Run `python manage.py migrate` to apply new migrations (if any).

4. Run `sudo systemctl restart gunicorn`. This will gracefully restart Gunicorn
    and pick up the changes.

Now your server should be running the updated backend API.

### Updating the Frontend

You just need to repeat the steps in [Frontend](#frontend) and overwrite the
files in the static file directory (e.g. `/var/www/html`) with the new `build`.

## Setting Up Accounts

After deploying the application, you need to set up super user accounts for
administrators (i.e. yourself) and accounts for ELC instructors to create and
manage surveys.

### Create Superuser Account

Go back to the backend directory and run the following command:

``` bash
python manage.py createsuperuser
```

Then follow the instructions to set up an superuser account. You need to provide
a username and a password, but an email address is optional (hit enter to skip).

If you later forget the superuser password, just repeat this step to create a
new one.

> Note: Remember to activated the virtual environment if you haven't already.

### Create Accounts for Instructors

1. Go to `https://example.com/django-admin/` (replace with your domain) and log
    in with the superuser account you created.

2. Under 'Authentication and Authorization' you will find 'Users'. Click that
    and you should be presented with a list of existing users.

3. Click 'ADD USER' button on the top right.

4. Enter username and password for the new account and click 'SAVE'.

After you click 'SAVE', the user is created and you don't need to change
anything else. Give the credentials of this account to ELC instructors and they
should be able to log in on the frontend and create surveys.

If an instructor forgets his or her password, find his or her account in the
list of users in step 2, click that username to open "Change user" page, and
than you can reset the password following the link that says "you can change the
password using this form" (next to "Password").
