# -*- encoding: utf-8 -*-
#!/bin/bash
#CentOS7上安装nginx gunicorn 部署django项目  2018.12.30
#
# 安装nginx，需要进行下列配置
# vim /etc/bashrc       //添加下列路径
# export PATH=$PATH:/usr/local/bin:/usr/bin:/usr/sbin:/etc/nginx;
# vim /etc/sudoers    //例如添加用户wuchunlong123
# wuchunlong123 ALL=(ALL)ALL  
# vim /etc/selinux/config   
# SELINUX=disabled      

import os
import datetime
from fabric.api import (cd, env, lcd, put, prompt, local, sudo, run,
                        prefix, shell_env, settings, hide, hosts, get)


from fabric.utils import warn

project_name = env.project_name
local_app_dir = './'
local_config_dir = './deployconfig'

remote_app_dir = '/home/www'
remote_website_dir = '%s/%s' %(remote_app_dir, project_name)

remote_nginx_dir = '/etc/nginx'
remote_gunicorn_dir = '/etc/systemd/system'

nowDate = datetime.datetime.now()
NOW_MARK = '%04d%02d%02d[%02d%02d%02d]' % (nowDate.year, nowDate.month,
                                         nowDate.day, nowDate.hour, 
                                         nowDate.minute, nowDate.second)

git_url_user_password = env.git_url_user_password
git_last = git_url_user_password.split('/')[-1]  #Mytest

remote_crontab_dir = '/etc'
crontab_conf = '%s root python3 %s/src/mysite/backupdb.py' %(env.crontab_time,remote_website_dir)
recover_db_name = 'db.txt_2019-01-11[13:08:02]' #一键恢复数据库文件

def install_python366(): 
    sudo('chmod -R 777 /home') 
    sudo('chmod -R 777 /home/%s' %(env.user))
    sudo('yum update -y && yum -y groupinstall "Development tools" '
        '&& yum install openssl-devel bzip2-devel expat-devel gdbm-devel '
        'readline-devel sqlite-devel psmisc ')
    sudo('if [ ! -f /usr/local/python3/bin/python3.6 ]; then  '
        'wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz && '
        'tar -zxvf Python-3.6.6.tgz && '
        'cd Python-3.6.6 && '
        './configure --prefix=/usr/local/python3 && '
        'make '
        '&& make install && '
        'ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3 && '
        'ln -s /usr/local/python3/bin/pip3.6 /usr/bin/pip3 && '
        'cd - ;fi')

def install_requirements_CentOS():  
    sudo('pip3 install virtualenv  --upgrade pip')
    sudo('yum install epel-release')
    sudo('[ ! -d /etc/nginx ] && '
        'yum install nginx && '
        'usermod -a -G root nginx || [ false ]')            
    sudo('pip3 install gunicorn')   
    sudo('yum install -y git')
    sudo('yum install -y gettext')

def init_remote_website_dir():
    sudo('rm -rf %s' %(remote_website_dir))
    sudo('mkdir -p "%s"' %(remote_app_dir))  
    sudo('chmod -R 777 %s' %(remote_app_dir))
    sudo('mkdir -p "%s"' %(remote_website_dir))
    sudo('chown -R %s:%s %s' %(env.user, env.user, remote_website_dir))
    with cd(remote_website_dir):
        run('/usr/local/python3/bin/virtualenv '
            '-p /usr/bin/python%s env' %(env.python_ver))
        run('mkdir -p logs')

def copy_git_project_dir():
    with cd(remote_website_dir):
        run(r'[ ! -d src  ] && git clone {} src '
            '|| [ false ]'.format(env.git_url))
        run(r'cd src && git pull && cd -')
        with prefix(r'source env/bin/activate'):
            run(r'pip3 install gunicorn')
            run(r'pip3 install -r src/requirements.txt')
            run(r'cd src/mysite && rm -rf static '
                '&& python3 manage.py collectstatic '
                '&& cd -')
        run(r'cp src/mysite/db.sqlite3 src/mysite/production.sqlite3')

def config_gunicorn(): #/etc/systemd/system/gunicorn.service
    sudo('systemctl stop gunicorn')    
    with lcd(local_config_dir):
        confStr = open('%s/gunicorn.service' %(local_config_dir)).read() 
        confStr = confStr.replace("{remote_website_dir}", remote_website_dir)
        open('%s/gunicorn.service.tmp' %(local_config_dir), "w").write(confStr)
        with cd(remote_gunicorn_dir):
            put('gunicorn.service.tmp', 'gunicorn.service', use_sudo=True)
    sudo('systemctl daemon-reload')
    sudo('systemctl start gunicorn')
    sudo('systemctl enable gunicorn') 

def config_nginx():  #/etc/nginx/nginx.conf
    sudo('systemctl stop nginx')
    with lcd(local_config_dir):
        confStr = open('%s/nginx.conf' %(local_config_dir)).read()     
        confStr = confStr.replace("{user}", env.user)
        confStr = confStr.replace("{remote_website_dir}", remote_website_dir)
        confStr = confStr.replace("{domain}", env.domain) 
        open('%s/nginx.conf.tmp' %(local_config_dir), "w").write(confStr)
        with cd(remote_nginx_dir):
            put('nginx.conf.tmp', 'nginx.conf.tmp', use_sudo=True)
            # nginx.conf 内容有变化就备份，没有变化不备份
            sudo(r'diff nginx.conf nginx.conf.tmp > /dev/null && '
                '[ $? ] && '
                'echo "nginx.conf == nginx.conf.tmp" || '
                'mv nginx.conf nginx.conf.%s && '
                'mv nginx.conf.tmp nginx.conf ' %(NOW_MARK))
    sudo('systemctl start nginx')
    sudo('systemctl enable nginx')

def create_git_repo(): 
    with cd(remote_website_dir):
        run(r'[ ! -d %s ] '
            '&& git clone %s '
            '|| [ false ]' % (git_last, git_url_user_password))

#在远程主机仓库，创建一个初始的 数据库压缩文件(含密码) db.txt
def create_db_txt(): 
    with cd(remote_website_dir):
        with cd('./%s' %(git_last)):
            sudo('mkdir -p db && '  
            'chmod -R 777 db && '
            'cp ../src/mysite/db.sqlite3 ./production.sqlite3 && '
            'tar -zcvf - db|openssl des3 -salt -k "8yhn(IJN&U*" | dd of=db.txt')  

def configure_centos7_crontab(): 
    sudo('/bin/systemctl stop crond.service')
    with lcd(local_config_dir):
        confStr = open('%s/crontab' %(local_config_dir)).read()
        confStr = confStr.replace("{crontab_conf}", crontab_conf)
        open('%s/crontab.tmp' %(local_config_dir), "w").write(confStr)
        with cd(remote_crontab_dir):
            sudo(r'[ ! -f ./crontab.bak ] && cp ./crontab ./crontab.bak || [ false ]')  #备份原始的crontab文件
            put('./crontab.tmp', './crontab', use_sudo=True)   
            sudo('chmod 644 ./crontab') 
            sudo('chown root:root ./crontab')
            sudo('/bin/systemctl restart crond.service')
            sudo('/bin/systemctl start crond.service')

# 一键恢复备份
def recover_sqlite_db():  
    with cd(remote_website_dir):
        sudo('cp ./%s/%s ./db.txt' %(git_last,recover_db_name))
        sudo('[ -f db.txt ] &&'
        'dd if=db.txt |openssl des3 -d -k "8yhn(IJN&U*"|tar zxf - && '
        'chmod 744 db/production.sqlite3 && '
        'cp db/production.sqlite3 src/mysite/production.sqlite3 && '
        'rm -rf db* || [ false ]')

#如果您正在运行防火墙，请运行以下命令以允许HTTP和HTTPS通信
def firewall_cmd():
    sudo('firewall-cmd --permanent --zone=public --add-service=http && '
        'firewall-cmd --permanent --zone=public --add-service=https && '
        'firewall-cmd --reload')

# fab -c fabricrc push_deploy
def push_deploy():
    with lcd(local_app_dir):
        local('git add .')
        local('git commit -am "{}"'.format(NOW_MARK))
        local('git push')

# fab -c fabricrc deploy_centos7
def deploy_centos7():
    install_python366()
    install_requirements_CentOS()
    init_remote_website_dir()
    copy_git_project_dir()
    create_git_repo()
    create_db_txt()
    configure_centos7_crontab()
    config_gunicorn()  
    config_nginx()

