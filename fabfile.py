import tempfile
import os
import datetime
from fabric.api import prefix, cd, lcd, local, require, env, put, run
from fabric.contrib.console import confirm
from fabric.decorators import task, hosts
from fabric.utils import puts, indent
from fabric.colors import blue, red, green

import poeg

"""
CONFIG, ENVIROMENTS
"""


TS = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
env.forward_agent = True
env.use_ssh_config = True

env.project_name = 'poeg'
env.branch = 'production'
env.git_repo = 'git@bitbucket.org:psenicka/poeg.git'
env.venv_python_version = 'python3'
env.manage_cmd = 'python manage.py'
env.version = poeg.__versionstr__
env.project_dir = '/var/www/%s' % env.project_name

env.pip_package_name = '%(project_name)s-%(version)s-py2.py3-none-any.wh' % env


@task
@hosts('poeg')
def deploy(upgrade_pip=False):

    # local('python setup.py bdist_wheel')
    # put('dist/%(pip_package_name)s', '/tmp/%(pip_package_name)s' % env)

    # Prepare new virtualenv and install all necessary things.
    # venv_path = '/srv/venv.%s' % TS
    # run('/opt/python/bin/virtualenv %s' % venv_path)
    with prefix('cd %(project_dir)s' % env):
        run('git pull')
        with prefix('source %s' % os.path.join('.env', 'bin', 'activate')):

            if upgrade_pip:
                run('pip install -U pip')

            run('pip install -r requirements-prod.txt')
            # run('pip install -U /tmp/%(pip_package_name)s' % env)

            print(blue('Collecting static files...'))
            run('%s collectstatic --noinput' % env.manage_cmd)

            print(blue('Compiling translation files...'))
            run('%s compilemessages' % env.manage_cmd)

            print(blue('Running migrations...'))
            run('%s migrate' % env.manage_cmd)

    # Switch the symlink to current virtualenv and restart app
    # FIXME? I'm not sure if virtualenv supports simlinking in this way,
    # but it seems it works, hardcoded paths work here
    # run('ls -ld venv')
    # print(blue("Changing virtualenv symlink to %s" % venv_path))
    # first time venv is real directory
    # run('rm -rf venv')
    # run('ln -s %s venv' % venv_path)
    run('supervisorctl restart %s' % env.project_name)

    # print("You can check if new environment runs fine and delete old ones.")
    # cleanup_old_environments()
