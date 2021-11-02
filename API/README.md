# GreenFi API 

## API Manual

`/`: Help, returns this manual as string
Everything below will return json string containing parameter, Timestamp, and CO2 ppm
`/ss`: Single Source, 
`/ssrt`: Single Source RealTime, 
`/g`: Global combined CO2, 
`/grt`: Global RealTime, 

## Build and Deploy

### Local Development
This is a flask application so using `flask run` will spin off the server,
This app uses sqlite database, which should come with python3.x
Deployment requires gunicorn which can be installed using pip

### Herku Deployment
This app is deployed on Heroku with gunicorn currently with the url https://greenfi-api.herokuapp.com/
Per the deployment specifications on heroku:

Download and install the Heroku CLI 

Mac: `brew tap heroku/brew && brew install heroku`

Ubuntu: `sudo snap install --classic heroku`

Windows: https://devcenter.heroku.com/articles/heroku-cli

Clone source code into repo (NOTICE: this is a git repository within a larger git repository, please clone to co2-oracle/API directory)
```
$ heroku git:clone -a greenfi-api
$ cd greenfi-api
```

Deploy changes
```
$ git add .
$ git commit -am "make it better"
$ git push heroku master
```
