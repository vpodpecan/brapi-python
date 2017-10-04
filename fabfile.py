from fabric.api import *

project_dir = '/srv/django-projects/brapi'
env.hosts = ['vid@vid@klapacij']


def deploy():
    with cd(project_dir), virtualenv():
        run('git pull origin master')
        run('cp --no-clobber conf/nginx.conf.sample conf/nginx.conf')
        run('cp --no-clobber conf/supervisor.conf.sample conf/supervisor.conf')
        run('pip install -r requirements.txt')
        run('python manage.py migrate')
        run('python manage.py collectstatic --noinput')
        # this is required when new supervisor task is added and we do not restart supervisord
        sudo('supervisorctl reread')
        sudo('supervisorctl update')
        sudo('supervisorctl restart termiolar_gunicorn termiolar_worker termiolar_monitor')
        sudo('nginx -t')
        sudo('nginx -s reload')
        sudo('ln -f -s {}/scripts/backup_termiolar /usr/local/bin'.format(project_dir))
        sudo('ln -f -s {}/scripts/restore_termiolar_database /usr/local/bin'.format(project_dir))
        sudo('ln -f -s {}/scripts/restore_termiolar_media /usr/local/bin'.format(project_dir))


def virtualenv():
    return prefix('source {}/termiolar-env/bin/activate'.format(project_dir))
