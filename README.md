# Proj

```
pipenv install -e git+https://github.com/andreif/proj.git#egg=proj

heroku labs:enable runtime-dyno-metadata
heroku labs:enable metrics-beta
# heroku labs:enable log-runtime-metrics
heroku labs
heroku run "env | sort"
```
