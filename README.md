# Proj

```
pipenv install -e git+https://github.com/andreif/proj.git#egg=proj

heroku labs:enable runtime-dyno-metadata
heroku labs:enable metrics-beta
# heroku labs:enable log-runtime-metrics
heroku labs
heroku run "env | sort"
```


```
heroku config:set DJANGO_SECRET_KEY=...
heroku config:set DJANGO_ALLOWED_HOSTS=...
heroku config:set DJANGO_SETTINGS_MODULE=...
```


Updating dependecies:
 - remove Pipenv.lock
 - run `pipenv install`

## New project

- copy example repo
- `git init && git add . && git commit -m initial`
- replace example with project name 
- change admin url
- start postgres
- `make setup`
- `make server`
