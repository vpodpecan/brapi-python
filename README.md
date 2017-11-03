

### OPEN QUESTIONS

-   incompleteness and errors in current DB schema
-   inconsistencies between BRAPI API description and current schema
e.g. germplasm -> typeOfGermplasmStorageCode is text, API wants array of strings



### How to install a production version

#### Requirements

1. `Postgres`
2. `Nginx`
3. `Python 3.5+`
4. `pip`
5. `uwsgi`
6.  python packages listed in `requirements.txt`

Please consult the corresponding documentation about how to install these requirements on your system. Note that on Ubuntu systems you will have to install packages such as python3-dev, python-pip, etc.

The following steps are to be performed only at the first installation. All subsequent updates of the project code are deployed using `fabric` (see below).


#### Database configuration

1. Create a user in Postgres named e.g., `django` and pick a password:
    ```sql
    CREATE USER django WITH PASSWORD 'password';
    ```
2. Create a database called `brapi`:
    ```sql
    CREATE DATABASE brapi;
    ```
3. Grant the user `django` all privileges, ensure `utf-8` encoding and configure few other parameters:
    ```sql
    GRANT ALL PRIVILEGES ON DATABASE brapi TO django;
    ALTER ROLE django SET client_encoding TO 'utf8';
    ALTER ROLE django SET default_transaction_isolation TO 'read committed';
    ALTER ROLE django SET timezone TO 'UTC';
    ```

#### Project configuration

1.  Clone the project to some folder, e.g., `/srv/django-projects/brapi`, set permissions and set up a virtual environment. You will have to know the user and group the nginx server is using, e.g., `nobody:nobody` on Slackware Linux and `www-data:www-data` on Ubuntu. We will assume `www-data:www-data` as the user and group and that we are logged in as user `someuser` (*please change these values according to your situation in the instructions below*).

    ```sh
    # make folder, download project sources, set permissions
    cd /srv
    sudo mkdir django-projects
    sudo chown -R someuser:www-data django-projects
    git clone git@bitbucket.org:vpodpecan/brapi.git django-projects/brapi
    sudo chown -R someuser:www-data django-projects
    sudo chown -R www-data django-projects/brapi/media_root

    # create and activate virtual environment
    cd /srv/django-projects/brapi
    python3 -m venv brapi-venv
    source brapi-venv/bin/activate

    # install all project requirements and gather static files
    pip install -r requirements.txt
    python manage.py collectstatic
    ```

2.  Copy the `__local_settings.py` into `local_settings.py` and edit according to your needs
    ```sh
    cd /srv/django-projects/brapi/brapi
    cp __local_settings.py local_settings.py
    nano local_settings.py
    ```
    You will have to provide your Postgres credentials and set the database engine to `psycopg2`. For example:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'django',
            'NAME': 'brapi',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': ''
        }
    }
    ```

    You will also have to add your server name to the ALLOWED_HOSTS variable, e.g.
    ```python
    ALLOWED_HOSTS = ['brapi.mydomain.net']
    ```
    You may use `ALLOWED_HOSTS = ['*']` but in this case you are responsible to provide your own validation of the `Host` header to help against HTTP Host header attacks.

3.  Build the application database and create a Django admin account
    ```sh
    cd /srv/django-projects/brapi/brapi
    source brapi-venv/bin/activate
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```


#### Web server

1.  Copy your `nginx.conf.sample` into `nginx.conf` and edit according to your settings. In general, you will only need to modify the server name and directory names.
    ```sh
    cd /srv/django-projects/brapi/conf
    cp nginx.conf.sample nginx.conf
    nano nginx.conf
    ```

2. Link the configured `nginx.conf` project file into your system's nginx sites folder, e.g. `/etc/nginx/sites-enabled/` on Ubuntu (or `/etc/nginx/conf.d` on Slackware) where it will be automatically loaded when nginx starts.
    ```sh
    cd /etc/nginx/sites-enabled/
    sudo ln -s /srv/django-projects/brapi/conf/nginx.conf
    ```

3. Test your configuration by visiting [http://localhost](http://localhost).
    If you see the *502 Bad Gateway* page it means that nginx is working and you should proceed to the next step to configure the application server. The error message simply tells you that nginx forwarded the request but the socket did not work so the request was not served by your Django app.

You shuld see the *"Welcome to nginx!"* page.




#### Application server

We will use the `uWSGI` applicaton server to serve our Django application to requests comming from our `nginx` HTTP server.

1.  First, copy your `uwsgi.ini.sample` into `uwsgi.ini` and edit according to your settings. Note that if you are using the suggested directory and socket file locations there is no need to change the default configuration.
    ```sh
    cd /srv/django-projects/brapi/conf
    cp uwsgi.ini.sample uwsgi.ini
    nano uwsgi.ini
    ```

2.  Run the `uwsgi` server
    ```sh
    cd /srv/django-projects/brapi/conf
    uwsgi --ini uwsgi.ini
    ```
    and test the configuration by visiting [http://localhost/admin](http://localhost/admin)

3.     

Typically, you will have to provide values for variables `ENGINE`, `USER`, `NAME`, `PASSWORD`, `HOST`. Use the values specified in the *Database configuration* section.

You will also have to add your server name to the ALLOWED_HOSTS variable, e.g.
```python
ALLOWED_HOSTS = ['brapi.mydomain.net']
```
You may use `*` but in this case you are responsible to provide your own validation of the `Host` header.

3.  Test whether everything is set up correctly by running Gunicorn from the command line:
```sh
cd /srv/django-projects/brapi
source brapi-venv/bin/activate
gunicorn --env DJANGO_SETTINGS_MODULE=brapi.settings brapi.wsgi --config conf/gunicorn.conf.py
```
The BRAPI link to list programs [/brapi/v1/programs](http://127.0.0.1/brapi/v1/programs) should return an JSON listing the first page of programs.

If you get a "502 bad gateway" error the likely cause is wrong file permissions or some other major error on the Django/Gunicorn. The traceback in the console or log of Gunicorn should give you a hint what went wrong.






TODO!

dodaj django-adminrestrict !

1.  First, ensure that nginx is up and running your edited `nginx.conf` file from the previous step. Please note that the command may differ from one Linux distribution to another.

    For Slackware Linux, the command is:
    ```sh
    sudo /etc/rc.d/rc.nginx restart
    ```
    For Ubuntu 16 or newer the command is:
    ```sh
    sudo systemctl restart nginx
    ```
    On older Ubuntu systems this should work:
    ```sh
    sudo /etc/init.d/nginx restart
    ```

    Your `nginx.conf` contains a line which tells which port is used for proxy. For example:
    ```
    proxy_pass http://127.0.0.1:8002;
    ```
    configures nginx to forward the traffic to local port 8002 where our application server (Gunicorn) is running. Gunicorn configuration file `conf/gunicorn.conf.py` also contains a line like
    ```python
    bind = "127.0.0.1:8002"
    ```
    Obviously, those two configuration lines have to specify the same address and port (the address may differ if you intend to run web and application servers on different computers).

2.  Prepare a 'local_settings.py' file with production specific settings (e.g. database connection and passwords):
    ```sh
    cd /srv/django-projects/brapi/brapi
    cp __local_settings.py local_settings.py
    nano local_settings.py
    ```
    Typically, you will have to provide values for variables `ENGINE`, `USER`, `NAME`, `PASSWORD`, `HOST`. Use the values specified in the *Database configuration* section.

    You will also have to add your server name to the ALLOWED_HOSTS variable, e.g.
    ```python
    ALLOWED_HOSTS = ['brapi.mydomain.net']
    ```
    You may use `*` but in this case you are responsible to provide your own validation of the `Host` header.

3.  Test whether everything is set up correctly by running Gunicorn from the command line:
    ```sh
    cd /srv/django-projects/brapi
    source brapi-venv/bin/activate
    gunicorn --env DJANGO_SETTINGS_MODULE=brapi.settings brapi.wsgi --config conf/gunicorn.conf.py
    ```
    The BRAPI link to list programs [/brapi/v1/programs](http://127.0.0.1/brapi/v1/programs) should return an JSON listing the first page of programs.

    If you get a "502 bad gateway" error the likely cause is wrong file permissions or some other major error on the Django/Gunicorn. The traceback in the console or log of Gunicorn should give you a hint what went wrong.

4.  Finally, you will probably want a monitor to supervise Gunicorn. See the [official Gunicorn documentation](http://docs.gunicorn.org/en/stable/deploy.html) for more details.
    TODO!


### How to update an existing installation

TODO!
Updating a working installation is easy. Only the following steps are required:
```sh
cd /srv/django-projects/brapi
source brapi-venv/bin/activate
sudo fab deploy
```

## THIS IS OBSOLETE



#### Requirements
-   Apache 2.4
-   mod_wsgi 4.5.20 (installed with pip inside virtual environment)

It is assumed that we will be using Python inside a virtual environment where mod_wsgi is also installed.

#### Steps
1.  Enable your Apache server (check the manual how to do it for your OS)
2.  Locate the Apache config file, e.g. `/etc/httpd/httpd.conf` (the location and name may be different on your OS)
3.  run `mod_wsgi-express module-config` to get the `mod_wsgi` module configuration settings, e.g.,
    ```sh
    LoadModule wsgi_module "/home/user/virtualenvs/brapi/lib/python3.5/site-packages/mod_wsgi/server/mod_wsgi-py35.cpython-35m-x86_64-linux-gnu.so"
    WSGIPythonHome "/home/user/virtualenvs/brapi"
    ```
    You have to paste these two lines into your Apache configuration file.

    Note, however, that if you want to run different Python applications with different virtual environments, this approach cannot be used. In this case, you will have to use `mod_wsgi-express` to launch applications on different ports and configure a proxy. Check the `mod_wsgi` documentation how to accomplish that.


    # make main application folder and set permissions
    cd /home
    mkdir web
    chown -R vid:apache web
    chmod -R 2750 web

    #
    cd web
    git clone git@bitbucket.org:vpodpecan/brapi.git
    python3 -m venv brapi-venv

    # activate virtualenv, install dependencies and copy static files
    source brapi-venv/bin/activate
    cd brapi
    pip install -r requirements.txt
    python manage.py collectstatic

    # give write permission for apache user
    chmod -R 2750 brapi/media_root
