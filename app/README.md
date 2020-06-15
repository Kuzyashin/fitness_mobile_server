# Boilerplate of Django project with REST API

## Deploy on production

`virtualenv --python=python3 --no-site-packages ./.env`

`.env/bin/pip install -r requirements.txt`

`.env/bin/pip install gunicorn`


### Add conf for nginx
```
server {
    listen 80;
    client_max_body_size 4G;
    server_name PROJECT_NAME.fullstack-development.com;
    error_log  /srv/PROJECT_NAME/logs/nginx_error.log;
    access_log  /srv/PROJECT_NAME/logs/access.log;
    keepalive_timeout 5;
    charset utf-8;

    root /srv/PROJECT_NAME;

    location / {
        proxy_read_timeout 1200;
        proxy_connect_timeout 1200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";


        proxy_pass http://unix:/srv/PROJECT_NAME/connection.sock;
    }

    location /static/ {
        alias /srv/PROJECT_NAME/public/static/;
    }
    location /media/ {
        alias /srv/PROJECT_NAME/public/media/;
    }
}
```
Enable config `ln -s /etc/nginx/sites-available/PROJECT_NAME.conf /etc/nginx/sites-enabled/`

Test configs `nginx -t`

`service nginx restart`



### Add conf for supervisor
```
[program:PROJECT_NAME]
command=/srv/PROJECT_NAME/.env/bin/gunicorn project.wsgi:application --bind unix:/srv/PROJECT_NAME/connection.sock --workers=3 --pid=/srv/PROJECT_NAME/pids/gunicorn.pid --log-file /srv/PROJECT_NAME/logs/gunicorn.log
directory=/srv/pionline
environment=PATH="/srv/PROJECT_NAME/.env/bin",LANG="ru_RU.utf8",LC_ALL="ru_RU.UTF-8", LC_LANG="ru_RU.UTF-8"
umask=022
autostart=true
autorestart=true
startsecs=10
startretries=3
exitcodes=0,2
stopsignal=TERM
stopwaitsecs=10
user=root

stdout_logfile = /srv/PROJECT_NAME/logs/gunicorn_out.log
stderr_logfile = /srv/PROJECT_NAME/logs/gunicorn_err.log
```
`supervisorctl reread`

`supervisorctl reload`

`supervisorctl status`


### Deploy.sh
Don't forget to change supervisor command in `deploy.sh`
