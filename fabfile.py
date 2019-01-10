# -*- encoding: utf-8 -*-
#!/bin/bash
#CentOS7上安装nginx gunicorn 部署django项目  2018.12.30
import os
import datetime
from fabric.api import (cd, env, lcd, put, prompt, local, sudo, run,
                        prefix, shell_env, settings, hide, hosts)
#from fabric.api import *

from fabric.utils import warn

project_name = '%s-%s' %(env.project_name, env.uuid)
local_app_dir = './'
local_config_dir = './deployconfig'
#local_app_dir = './%s' %(env.git_url.split('/')[-1])

src_tar_file = './%s' %(env.src_tar_file) #注意：先将工程目录设为src后再压缩

remote_app_dir = '/home/www'
remote_git_dir = '/home/git'
remote_website_dir = '%s/%s' %(remote_app_dir, project_name)

remote_nginx_dir = '/etc/nginx'
remote_gunicorn_dir = '/etc/systemd/system'

nowDate = datetime.datetime.now()
NOW_MARK = '%04d%02d%02d%02d%02d%02d' % (nowDate.year, nowDate.month,
                                         nowDate.day, nowDate.hour, 
                                         nowDate.minute, nowDate.second)

#初始状态目录，是登录用户wcl6005的‘家’目录,即： cd ~   /home/wcl6005/Python-3.6.6.tgz
def install_python366(): #安装python3.6.6  fab -c fabricrc install_python366
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
    install_python366()
    sudo('pip3 install virtualenv  --upgrade pip')
    sudo('yum install epel-release')
    sudo('if [ ! -d /etc/nginx ]; then '
        'yum install nginx && '
        'firewall-cmd --permanent --zone=public --add-service=http && '
        'firewall-cmd --permanent --zone=public --add-service=https && '
        'firewall-cmd --reload; fi')
    sudo('usermod -a -G root nginx')            
    sudo('pip3 install gunicorn')   
    sudo('yum install -y git')
    sudo('yum install -y gettext')
    sudo('rm -rf %s' %(remote_website_dir))
    sudo('mkdir -p "%s"' %(remote_app_dir))  
    sudo('chmod -R 777 %s' %(remote_app_dir))
    sudo('mkdir -p "%s"' %(remote_website_dir))
    sudo('chown -R %s:%s %s' %(env.user, env.user, remote_website_dir))
    with cd(remote_website_dir):
        run('/usr/local/python3/bin/virtualenv '
            '-p /usr/bin/python%s env' %(env.python_ver))
        run('mkdir -p logs')

def into_virtualenv():
    with prefix(r'source env/bin/activate'):
        run(r'pip3 install gunicorn')
        run(r'pip3 install -r src/requirements.txt')
        run(r'cd src/mysite && rm -rf static '
            '&& python3 manage.py collectstatic '
            '&& cd -')
    run(r'cp src/mysite/demo.sqlite3 src/mysite/production.sqlite3')

def copy_local_project_dir():#把本地的工程压缩代码拷贝到远程主机src目录
    with cd(remote_website_dir):
        put(src_tar_file, './')
        run("tar -zxvf %s && rm -rf %s" %(src_tar_file,src_tar_file))
        into_virtualenv()

def copy_git_project_dir():#把git上的工程代码拷贝到远程主机src目录
    with cd(remote_website_dir):
        run(r'[ ! -d src  ] && git clone {} src '
            '|| [ false ]'.format(env.git_url))
        run(r'cd src && git pull && cd -')
        into_virtualenv()

def config_gunicorn(): #/etc/systemd/system/gunicorn.service
    sudo('systemctl stop gunicorn')    
    with lcd(local_config_dir):
        confStr = open('%s/gunicorn.service' %(local_config_dir)).read() 
        confStr = confStr.replace("{remote_website_dir}", remote_website_dir)
        open('%s/gunicorn.service.tmp' %(local_config_dir), "w").write(confStr)
        with cd(remote_gunicorn_dir):
            put('gunicorn.service.tmp', 'gunicorn.service', use_sudo=True)
    sudo('systemctl start gunicorn')
    sudo('systemctl enable gunicorn') 

def config_nginx():  #/etc/nginx/nginx.conf
    sudo('systemctl stop nginx')
    with lcd(local_config_dir):
        confStr = open('%s/nginx.conf' %(local_config_dir)).read()     
        confStr = confStr.replace("{user}", env.user)
        confStr = confStr.replace("{remote_website_dir}", remote_website_dir)
        #confStr = confStr.replace("{gunicorn_port}", env.gunicorn_port) #？
        confStr = confStr.replace("{domain}", env.domain) 
        open('%s/nginx.conf.tmp' %(local_config_dir), "w").write(confStr)
        with cd(remote_nginx_dir):
            put('nginx.conf.tmp', 'nginx.conf.tmp', use_sudo=True)
            # nginx.conf 内容有变化就备份，没有变化不备份
            sudo(r'diff nginx.conf nginx.conf.tmp > /dev/null && '
                '[ $? ] && '
                'echo "nginx.conf == nginx.conf.tmp" || '
                'mv nginx.conf nginx.conf.%s; '
                'mv nginx.conf.tmp nginx.conf ' %(NOW_MARK))

    #sudo('systemctl reload nginx') 
    sudo('systemctl start nginx')
    sudo('systemctl enable nginx')


def deploy_git(): #把git上的代码部署到远程主机  fab -c fabricrc deploy_git
    install_requirements_CentOS()
    copy_git_project_dir()
    config_gunicorn()  
    config_nginx()
    print('git -- ok!ok!ok!')

def deploy_put(): #把本地工程压缩代码部署到远程主机  fab -c fabricrc deploy_put
    install_requirements_CentOS()
    copy_local_project_dir()
    config_gunicorn()  
    config_nginx()
    print('put -- ok!ok!ok!')

def project_to_git():  # fab -c fabricrc project_to_git
    with lcd(local_app_dir):
        local('git add . && git commit -a -m "{}" && git push '.format(NOW_MARK) )

#---------下面是测试函数-----------#
def file_diff(): # 判断远程主机文件是否相等 相等ok 不相等no fab -c fabricrc file_diff
    with cd(remote_nginx_dir):
        sudo(r'diff nginx.conf nginx.conf > /dev/null && [ $? ] && echo "ok" || echo "no" ')
        #sudo(r'diff nginx.conf uwsgi.log > /dev/null && [ $? ] && echo "ok" || echo "no" ')



