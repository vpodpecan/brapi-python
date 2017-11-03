

### OPEN QUESTIONS

-   incompleteness and errors in current DB schema
-   inconsistencies between BRAPI API description and current schema
e.g. germplasm -> typeOfGermplasmStorageCode is text, API wants array of strings

## How to install BrAPI Django application

This manual describes the installation of the BrAPI Django application on a modern Linux system.

**Author**: Vid Podpečan (vid.podpecan@ijs.si)


#### Requirements

1. `Postgres`
2. `Nginx`
3. `Python 3.5+`
4. `pip`
5. `uwsgi`
6.  python packages listed in `requirements.txt`

Please consult the corresponding documentation about how to install these requirements on your system. Note that on Ubuntu systems you will also have to install packages such as `python3-dev`, `python-pip`, etc.

The following steps are to be performed only at the first installation. All subsequent updates of the project code are very simple as explained in the end of this manual.


### Database configuration

1. Create a user in Postgres named e.g., `django` and pick a password:
    ```sql
    CREATE USER django WITH PASSWORD 'password';
    ```
2. Create a database called `brapi`:
    ```sql
    CREATE DATABASE brapi;
    ```
3. Grant the user `django` create db privileges and set ownership, ensure `utf-8` encoding and configure few other parameters:
    ```sql
    ALTER USER django CREATEDB;
    ALTER DATABASE brapi OWNER TO django;
    ALTER ROLE django SET client_encoding TO 'utf8';
    ALTER ROLE django SET default_transaction_isolation TO 'read committed';
    ALTER ROLE django SET timezone TO 'UTC';
    ```

### Project configuration

1.  Clone the project to some folder, e.g., `/srv/django-projects/brapi`, set permissions and set up a virtual environment. You will have to know the user and group the nginx server is using, e.g., `nobody:nobody` on Slackware Linux and `www-data:www-data` on Ubuntu. We will assume `www-data:www-data` as the user and group and that we are logged in as user `someuser` (*please change these values according to your situation in the instructions below*).

    ```sh
    # make folder, download project sources, set permissions
    cd /srv
    sudo mkdir django-projects
    sudo chown -R someuser:www-data django-projects
    git clone git@bitbucket.org:vpodpecan/brapi.git django-projects/brapi
    sudo chown -R someuser:www-data django-projects
    sudo chown -R www-data django-projects/brapi/media_root

    # add user to nginx's group
    sudo usermod -a -G www-data someuser

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


### Web server

1.  Copy your `nginx.conf.sample` into `nginx.conf` and edit according to your settings. In general, you will only need to modify the server name and directory names.
    ```sh
    cd /srv/django-projects/brapi/conf
    cp nginx.conf.sample nginx.conf
    nano nginx.conf
    ```

2.  Link the configured `nginx.conf` project file into your system's nginx sites folder, e.g. `/etc/nginx/sites-enabled/` on Ubuntu (or `/etc/nginx/conf.d` on Slackware) where it will be automatically loaded when nginx starts.
    ```sh
    cd /etc/nginx/sites-enabled/
    sudo ln -s /srv/django-projects/brapi/conf/nginx.conf
    ```

3.  Restart nginx by typing
    ```sh
    sudo service nginx restart
    ```
    on Ubuntu Linux or
    ```sh
    sudo /etc/rc.d/rc.nginx restart
    ```
    on Slackware Linux and test your configuration by visiting [http://localhost](http://localhost).
    If you see the *502 Bad Gateway* page it means that nginx is working and you should proceed to the next step to configure the application server. The error message simply tells you that nginx forwarded the request which was then not handled by the application server.


### Application server

We will use the `uWSGI` applicaton server to serve requests comming to our Django application from our `nginx` HTTP server.

1.  First, copy your `uwsgi.ini.sample` into `uwsgi.ini` and edit according to your settings. Note that if you are using the suggested directory and socket file locations there is no need to change the default configuration.
    ```sh
    cd /srv/django-projects/brapi/conf
    cp uwsgi.ini.sample uwsgi.ini
    nano uwsgi.ini
    ```

2.  Run the `uwsgi` server
    ```sh
    sudo uwsgi --ini /srv/django-projects/brapi/conf/uwsgi.ini --uid www-data --gid www-data
    ```
    and test the configuration by visiting [http://localhost/admin](http://localhost/admin)

3.  If you want to start uwsgi at boot simply add the command to your `rc.local` script.

    For a better integration with your system's services manager please consult the official uWSGI documentation: [https://uwsgi-docs.readthedocs.io/en/latest/](https://uwsgi-docs.readthedocs.io/en/latest/)



dodaj django-adminrestrict !

### How to update an existing installation

Updating a working installation is easy. The following steps are required:

1.  Get the updates
    ```sh
    cd /srv/django-projects/brapi
    git pull
    ```
2.  Apply database migrations (if any)
    ```sh
    cd /srv/django-projects/brapi/brapi
    source brapi-venv/bin/activate
    python manage.py makemigrations
    python manage.py migrate
    ```

3.  Restart uWSGI and nginx
