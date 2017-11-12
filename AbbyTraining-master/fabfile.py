# -*- encoding: utf-8 -*-

from fabric.api import (cd, env, lcd, put, prompt, local, sudo, run,
                        prefix, shell_env, settings, hide)
from fabric.utils import warn


project_name = 'AbbyTraining'
local_app_dir = './'
local_config_dir = './deployconfig'

remote_app_dir = '/home/www'
remote_git_dir = '/home/git'
remote_flask_dir = '{}/{}'.format(remote_app_dir, project_name)
remote_nginx_enable_dir = '/etc/nginx/sites-enabled'
remote_nginx_avail_dir = '/etc/nginx/sites-available'
remote_supervisor_dir = '/etc/supervisor/conf.d'


def install_requirements_u1404():
    sudo('if [ -f /etc/apt/sources.list ];then cp /etc/apt/sources.list /etc/apt/sources.list.$(date +"%y%m%d%H%M%S");fi')
    with lcd(local_config_dir):
        with cd('/etc/apt'):
            put('./sources.list', './', use_sudo=True)
    sudo('apt-get update')
    sudo('apt-get install -y python python-dev python-pip')
    sudo('apt-get install -y python-virtualenv')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y supervisor')
    sudo('apt-get install -y git')

    sudo('rm -rf {}/env'.format(remote_flask_dir))
    sudo('mkdir -p "{}"'.format(remote_app_dir))
    sudo('chown -R {}:{} {}'.format(env.user, env.user, remote_app_dir))
    sudo('mkdir -p "{}"'.format(remote_flask_dir))
    sudo('chown -R {}:{} {}'.format(env.user, env.user, remote_flask_dir))
    with lcd(local_app_dir):
        with cd(remote_flask_dir):
            run('virtualenv env')
            run('mkdir -p logs')
            run('mkdir -p instance')
            put('demo/config.py', 'instance')   # init instance/config.py with demo
            run('mkdir -p edustack/db')
            put('demo/demo.db', 'edustack/db/') # init edustack db with demo.db

def copy_project_dir():
    with lcd(local_app_dir):
        local(r'mkdir -p putdir '
              '&& rm -rf putdir/*'
              '&& cp -r edustack putdir '
              '&& cp -r frontend/dist putdir '
              '&& mv putdir/dist putdir/front '
              '&& cp -r frontend-org/dist putdir '
              '&& mv putdir/dist putdir/example '
              '&& tar zcvf putdir.tgz putdir '
              '&& rm -rf putdir ')
        with cd(remote_flask_dir):
            put('config', './')
            put('putdir.tgz', './')
            run('tar zxvf putdir.tgz '
                '&& rm -rf edustack front example '
                '&& mv putdir/* .')
            put('demo/demo.db', 'edustack/db/')
            put('manage.py', './')
            put('requirements.txt', './')
            put('run.py', './')
        with cd(remote_flask_dir):
            with prefix('source env/bin/activate'):
                run('pip install -r requirements.txt')
            run('python manage.py prepare_theme')

def backup_sqlite_db():
    with lcd(local_app_dir):
        with cd(remote_flask_dir):
            run(r'[ -f edustack/db/demo.db ] '
                '&& [ ! -f edustack/db/demo.db.bak ] '
                '&& mv edustack/db/demo.db edustack/db/demo.db.bak '
                '|| [ false ]')

def recover_sqlite_db():
    with lcd(local_app_dir):
        with cd(remote_flask_dir):
            run('[ -f edustack/db/demo.db.bak ] '
                '&& mv edustack/db/demo.db.bak edustack/db/demo.db '
                '|| [ false ]')

def configure_nginx():
    sudo('/etc/init.d/nginx stop')
    sudo('rm -rf {}/{}'.format(remote_nginx_enable_dir, 'default'))
    sudo('rm -rf {}/{}'.format(remote_nginx_enable_dir, project_name))
    sudo('rm -rf {}/{}'.format(remote_nginx_avail_dir, project_name))
    with lcd(local_config_dir):
        confStr = open('{}/nginx.conf'.format(local_config_dir)).read()
        confStr = confStr.replace("{remote_flask_dir}", remote_flask_dir)
        open('{}/.nginx.conf.tmp'.format(local_config_dir), "w").write(confStr)
        with cd(remote_nginx_avail_dir):
            put('./.nginx.conf.tmp', './{}'.format(project_name), use_sudo=True)
    sudo('ln -s {}/{} {}/{}'.format(
        remote_nginx_avail_dir, project_name,
        remote_nginx_enable_dir, project_name
    ))
    sudo('/etc/init.d/nginx start')

def configure_supervisor():
    sudo('supervisorctl stop {}'.format(project_name))
    sudo('rm -rf {}/{}.conf'.format(remote_supervisor_dir, project_name))
    with lcd(local_config_dir):
        confStr = open('{}/supervisor.conf'.format(local_config_dir)).read()
        confStr = confStr.replace("{remote_flask_dir}", remote_flask_dir)
        confStr = confStr.replace("{project_name}", project_name)
        confStr = confStr.replace("{user}", env.user)
        open('{}/.supervisor.conf.tmp'.format(local_config_dir), "w").write(confStr)
        with cd(remote_supervisor_dir):
            put('./.supervisor.conf.tmp', './{}.conf'.format(project_name), use_sudo=True)
    sudo('supervisorctl reread')
    sudo('supervisorctl update')

def configure_git():
    """
    1. Setup bare Git repo
    2. Create post-receive hook
    3. Change owner of git repo
    """
    sudo('mkdir -p "{}"'.format(remote_git_dir))
    with cd(remote_git_dir):
        sudo('mkdir {}.git'.format(project_name))
        with cd('{}.git'.format(project_name)):
            sudo('git init --bare')
            with lcd(local_config_dir):
                with cd('hooks'):
                    put('./post-receive', './', use_sudo=True)
                    sudo('chmod +x post-receive')
        sudo('chown -R {}:{} ./'.format(env.user, env.user))

def run_app():
    with cd(remote_flask_dir):
        sudo('supervisorctl start {}'.format(project_name))

def restart_app():
    with cd(remote_flask_dir):
        sudo('supervisorctl restart {}'.format(project_name))

def install_mysql():
    sudo('apt-get install -y debconf-utils')
    with settings(hide('warnings', 'stderr'), warn_only=True):
        result = sudo('dpkg-query --show mysql-server')
    if result.failed is False:
        warn('MySQL is already installed')
        return
    mysql_password = prompt('Please enter MySQL root:')
    sudo('echo "mysql-server-5.5 mysql-server/root_password password ' \
        '{}" | debconf-set-selections'.format(mysql_password))
    sudo('echo "mysql-server-5.5 mysql-server/root_password_again password ' \
        '{}" | debconf-set-selections'.format(mysql_password))

    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        sudo('apt-get -y --no-upgrade install {}'.format(
            ' '.join(['mysql-server', 'mysql-client']))
        )
        sudo('mysql_secure_installation')
    sudo('apt-get install -y python-mysqldb')

def db_migrate():
    """ sync up database after update the production"""
    app_config_file = '{}/config/production.py'.format(remote_flask_dir)
    with cd(remote_flask_dir):
        with shell_env(APP_CONFIG_FILE=app_config_file):
            with prefix('source env/bin/activate'):
                run('python manage.py syncdb')
                run('python manage.py init')

def status():
    sudo('supervisorctl status')

def push_deploy():
    """
    1. Commit new files
    2. Restart gunicorn via supervisor
    """
    with lcd(local_app_dir):
        local('git add -A')
        commit_message = prompt("Commit message?")
        local('git commit -am "{}"'.format(commit_message))
        local('git push production master')
    db_migrate()
    restart_app()

def deploy():
    copy_project_dir()
    configure_nginx()
    configure_supervisor()
    restart_app()

def deployKeepDB():
    backup_sqlite_db()
    copy_project_dir()
    recover_sqlite_db()
    configure_nginx()
    configure_supervisor()
    restart_app()

def init_deploy_u1404():
    install_requirements_u1404()
    install_mysql()
    deploy()

