# Proj

## Setting up a new project

- copy example repo
- replace example with project name 
- change admin url
- start postgres
- `make setup`
- `make server`

Git

- `git init && git add . && git commit -m initial`
- create github repo
- git branch -M main
- git remote add origin git@github.com:{user}/{repo}.git
- git push -u origin main

Heroku

- create heroku app
- heroku git:remote -a myapp || git remote add heroku https://git.heroku.com/{app}.git
- select deploy method to github
- enable automatic deploys

```
heroku addons:add heroku-postgresql:hobby-dev
heroku addons:add memcachier:dev
heroku addons:add sentry:f1
heroku addons:add newrelic:wayne
```

```
heroku config:set DJANGO_SETTINGS_MODULE=example.settings
heroku config:set DJANGO_ALLOWED_HOSTS=example.com
heroku config:set DJANGO_SECRET_KEY=[random string of choice]
heroku config:set DISABLE_COLLECTSTATIC=1
```

Deploy

- git push to github or heroku
- heroku run python src/manage.py createsuperuser


Troubleshooting

```sh
heroku config
heroku run env | sort
```

Labs

```
heroku labs:enable runtime-dyno-metadata
heroku labs:enable metrics-beta
# heroku labs:enable log-runtime-metrics
heroku labs
```

### Upgrade requirements

 - remove Pipenv.lock
 - run `pipenv install`

### Stack update

heroku stack:set heroku-20

### From scratch

```
pipenv install -e git+https://github.com/andreif/proj.git#egg=proj
```
