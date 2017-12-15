## A Python+Django implementation of BrAPI

##### About
This project implements the Plantbreeding API using the Python language and the Django web framework.
See [https://github.com/plantbreeding/API]((https://github.com/plantbreeding/API)) for more information about BrAPI.

##### Status
This is a working but not yet complete implementation of BrAPI. As soon as the BrAPI itself becomes stable and complete and a full test data set is made available the sources can be easily upgraded.


##### Author

[Vid Podpečan](http://kt.ijs.si/vid_podpecan/) (vid.podpecan@ijs.si)  
[Jožef Stefan Institute](http://kt.ijs.si/) & [National Institute of Biology](http://www.nib.si/eng/index.php/departments/department-of-biotechnology-and-systems-biology)


##### License

The code is licensed under the GPLv3 lincense.


### How to set up Django BrAPI

This manual describes the installation and configuration of the BrAPI Django application on a modern Linux system, e.g. Ubuntu 16.04.


#### Requirements

1.  `Postgres`
2.  `Nginx`
3.  `Python 3.5+`
4.  `pip`
5.  `uWSGI`
6.  python packages listed in `requirements.txt`

Please consult the corresponding documentation about how to install these requirements on your system. Note that on Ubuntu systems you will also have to install packages such as `python3-dev`, `python-pip`, etc. The described steps are to be performed only at the first installation. All subsequent updates of the project code are very simple as explained at the end of this manual.

##### Development installation
If you only need a development installation of Django BrAPI, you can skip the installation of Postgres, Nginx and uWSGI. You will only have to modify your `local_settings.py` to use a SQLite database:
```python
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'databases', 'db.sqlite3'),
    }
}
```
and install all Python packages (see the instructions below). Then, create the database, launch the development server and visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
```sh
cd /srv/django-projects/brapi
source brapi-venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```




#### Database configuration

1.  Launch `psql`
    ```sh
    sudo -u postgres psql
    ```

2.  Create a database user named e.g., `django` and pick a password:
    ```sql
    CREATE USER django WITH PASSWORD 'password';
    ```
3.  Create a database called `brapi`:
    ```sql
    CREATE DATABASE brapi;
    ```
4.  Grant the user `django` create db privileges and set ownership, ensure `utf-8` encoding and configure few other parameters:
    ```sql
    ALTER USER django CREATEDB;
    ALTER DATABASE brapi OWNER TO django;
    ALTER ROLE django SET client_encoding TO 'utf8';
    ALTER ROLE django SET default_transaction_isolation TO 'read committed';
    ALTER ROLE django SET timezone TO 'UTC';
    ```

#### Project configuration

1.  Clone the project to some folder, e.g., `/srv/django-projects/brapi`, set permissions and set up a virtual environment. You will have to know the user and group the Nginx server is using, e.g., `nobody:nobody` on Slackware Linux and `www-data:www-data` on Ubuntu. We will assume `www-data:www-data` as the user and group and that we are logged in as user `someuser` (*please change these values according to your situation in the instructions below*).

    ```sh
    # make folder, download project sources, set permissions
    cd /srv
    sudo mkdir django-projects
    sudo chown -R someuser:www-data django-projects
    git clone https://github.com/vpodpecan/brapi-python.git django-projects/brapi
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

#### Web server

1.  Copy your `nginx.conf.sample` into `nginx.conf` and edit according to your settings. In general, you will only need to modify the server name and directory names.
    ```sh
    cd /srv/django-projects/brapi/conf
    cp nginx.conf.sample nginx.conf
    nano nginx.conf
    ```

2.  Link the configured `nginx.conf` project file into your system's nginx sites folder, e.g. `/etc/nginx/sites-enabled/` on Ubuntu (or `/etc/nginx/conf.d` on Slackware) where it will be automatically loaded when Nginx starts.
    ```sh
    cd /etc/nginx/sites-enabled/
    sudo ln -s /srv/django-projects/brapi/conf/nginx.conf
    ```

3.  Restart Nginx by typing
    ```sh
    sudo service nginx restart
    ```
    on Ubuntu Linux or
    ```sh
    sudo /etc/rc.d/rc.nginx restart
    ```
    on Slackware Linux and test your configuration by visiting [http://localhost](http://localhost).
    If you see the *502 Bad Gateway* page it means that Nginx is working and you should proceed to the next step to configure the application server. The error message simply tells you that Nginx forwarded the request which was then not handled by the application server.

4.  If you have an active firewall you may need to allow Nginx to communicate on ports 80 and 443. On Ubuntu systems use the following command:
    ```sh
    sudo ufw allow 'Nginx Full'
    ```

#### Application server

We will use the `uWSGI` applicaton server to serve the requests comming to our Django application from our Nginx HTTP server.

1.  First, copy your `uwsgi.ini.sample` into `uwsgi.ini` and edit according to your settings. Note that if you are using the suggested directory and socket file locations there is no need to change the default configuration.
    ```sh
    cd /srv/django-projects/brapi/conf
    cp uwsgi.ini.sample uwsgi.ini
    nano uwsgi.ini
    ```

2.  Run the uWSGI server
    ```sh
    sudo uwsgi --ini /srv/django-projects/brapi/conf/uwsgi.ini --uid www-data --gid www-data
    ```
    and test the configuration by visiting [http://localhost/admin](http://localhost/admin)

3.  If you want to start uWSGI at boot simply add the command to your `rc.local` script.

    For a better integration with your system's services manager please consult the official uWSGI documentation: [https://uwsgi-docs.readthedocs.io/en/latest/](https://uwsgi-docs.readthedocs.io/en/latest/)


#### How to update an existing installation

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


#### Database backup and restore

##### Backup

To create a backup of the whole `brapi` database you can use the `pg_dump` utility:
```sh
sudo -u postgres pg_dump --clean brapi | gzip > brapi-db-backup.gz
```

##### Restore

To restore from a backup archive into a `brapi` database use `psql`:
```sh
sudo -u postgres gunzip -c filename.gz | psql brapi
```

After the restoration make sure that the `django user` owns the `brapi` database:
```sh
sudo -u postgres psql
```
```sql
ALTER DATABASE brapi OWNER TO django;
```

###### Note
When restoring from a backup archive into a clean new system, first make sure that the `django` user exists and has enough privileges:
```sh
sudo -u postgres psql
```
```sql
CREATE USER django WITH PASSWORD 'password';
ALTER USER django CREATEDB;
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';
```



### How to update Django BrAPI to a new BrAPI specification


In general, only minor updates are expected, e.g., field renaming, type changes, add tables, etc. This means that very little work is required to update Django BrAPI to the new version.  

The following steps should be followed:

1.  Update Django BrAPI Models in `jsonapi/models.py`. Add new fields, rename, change type, add classes, etc.

2.  Migrate your changes into the database:
    ```sh
    cd /srv/django-projects/brapi
    source brapi-venv/bin/activate
    python manage.py makemigrations
    python manage.py migrate
    ```

3.  Update Django BrAPI serializers in `jsonapi/serializers.py`. Change name, add class, etc. You can reuse most of the code as the pattern is always the same.


4.  Update Django BrAPI views in `jsonapi/views.py`. This is the most time consuming step. Typically, you will have to write a new class which will handle the request parameters and retrieve objects from the database. Again, the majority of the new code can be reused from other view classes which already implement all possible API call variants and options.

5.  If required, update the `jsonapi/urls.py` by adding a new url pointing to a newly created view class.
