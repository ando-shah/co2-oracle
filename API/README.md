
# CO2 Oracle API


## API Manual

`/`: Help, returns this manual as string
Everything below will return json string containing parameter, Timestamp, and CO2 ppm
`/smoothed`: Smoothed data that shows seasonal variations in CO2 concentration : updated daily, 
`/trend`: Seasonally corrected CO2 concentration : updated daily 


## Build and Deploy

### Local Development
This is a flask application so using `flask run` will spin off the server,
This app uses sqlite database, which should come with python3.x
Deployment requires gunicorn and other python packaged which can be installed using pip:
```
pip install -r requirements.txt
```

It is encouraged to run this within it's own virtual environment


### Herku Deployment
This app is deployed on Heroku with gunicorn currently with the url https://greenfi-api.herokuapp.com/
Per the deployment specifications on heroku:

Download and install the Heroku CLI 

Mac: `brew tap heroku/brew && brew install heroku`

Ubuntu: `sudo snap install --classic heroku`

Windows: https://devcenter.heroku.com/articles/heroku-cli

Since this project is structured oddly (2 repos in one), Heroku doesnt like it. Please copy over the /API folder and initialize it as a git repo
```
$ git init
```
Then connect it to the Heroku app
```
$ heroku git:remote -a <heroku app name>
```

#### Deploy changes
```
$ git add .
$ git commit -am "make it better"
$ git push heroku master
```
#### Check if connected to Heroku:
```
git remote -v

```

## Current Issues
- SQlite is not supported by Heroku. As a result, there is no persistence in the data stored in the DB. Needs to migrate to SQLAlchemy
- Move to AWS?
