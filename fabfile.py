from fabric.api import lcd, local

def prepare_deployment(branch_name):
    local('python manage.py test Tickets')
    local('git add --all && git commit') 


def deploy():
    with lcd('/path/to/my/prod/area/'):

        local('git pull /my/path/to/dev/area/')
        local('python manage.py migrate myapp')
        local('python manage.py test myapp')
        local('/my/command/to/restart/webserver')s