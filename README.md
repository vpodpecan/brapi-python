

### OPEN QUESTIONS

-   incompleteness and errors in current DB schema
-   inconsistencies between BRAPI API description and current schema
e.g. germplasm -> typeOfGermplasmStorageCode is text, API wants array of strings



### How to install a production version

#### Requirements

1. `Postgres`
2. `Nginx`
3. `Python 3.5+`
4. python packages listed in `requirements.txt`

The following steps are to be performed only at the first installation. All subsequent updates of the project code are deployed using `fabric` (see below).


#### Database configuration

1. Create a user in Postgres named e.g., `django` and pick a password
    ```sql
    CREATE USER django WITH PASSWORD 'password';
    ```
2. Create a database called `brapi`
    ```sql
    CREATE DATABASE django;
    ```
3. Grant the user `django` all privileges and ensure `utf-8` encoding
    ```sql
    GRANT ALL PRIVILEGES ON DATABASE brapi TO django;
    ALTER ROLE django SET client_encoding TO 'utf8';
    ```

#### Project configuration

1. Clone the project to some folder, e.g., `/srv/django-projects/brapi`, set permissions and set up a virtual environment. We assume that `nginx` belongs to the `nobody` user group and `nobody` user account and that we are logged in as user `someuser`
```sh
sudo mkdir /srv/django-projects
sudo chown -R someuser:nobody /srv/django-projects
sudo chmod -R 2750 /srv/django-projects
git clone git@bitbucket.org:vpodpecan/brapi.git django-projects/brapi
sudo chown -R nobody /srv/django-projects/brapi/media_root
python3 -m venv django-projects/brapi/brapi-venv
source django-projects/brapi/brapi-venv/bin/activate
pip install -r django-projects/brapi/requirements.txt
python manage.py collectstatic
```

#### Web server

1. Link the `nginx.conf` project file into your system's nginx folder, e.g. `/etc/nginx/conf.d` where it will be automatically loaded when nginx starts.
```sh
cd /etc/nginx/conf.d
sudo ln -s /srv/django-projects/brapi/conf/nginx.conf
```

2. Copy `/srv/django-projects/brapi/conf/nginx.conf.sample` and edit according to your settings. In general, you will only need to modify server name and directory names.
```
cd /srv/django-projects/brapi/conf
cp nginx.conf.sample nginx.conf
nano nginx.conf
```


gunicorn --env DJANGO_SETTINGS_MODULE=brapi.settings brapi.wsgi --config /srv/django-projects/brapi/conf/gunicorn.conf.py







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
