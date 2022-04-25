# Casting Agency Project

## Introduction
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. This application includes,  
1) Two db models: Movie and Actor
2) API includes 6 endpoints  
3) Two job roles(Casting Assistant and Executive Producer) can access the API and each role has different permissions. 

### Project motivation  
This is the final project of the Udacity full stack nanodegree. I developed this project to make use of the knowledge I acquired in this nanodegree. Following technoligies were used in this project and by developing this project I gained confidence on using these skills on real-world projects.  

1) Postgres and Sqlalchemy - database modelling
2) Flask - develop web API to perform CRUD operations on database
3) Unittest - implement automated testing
4) Auth0 - implement authorization and role based authentification
5) Heroku - cloud platform used to deploy the web application to cloud

Application is hosted at: https://imesha-fsnd-cinema.herokuapp.com/ 

## Getting Started - Running project locally

* Clone the repository to local machine.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Postgres 14.2

Follow instructions to install the latest version of postgres for your platform in the [postgresql](https://www.postgresql.org/download/)

#### Heroku 7.60.1

Follow instructions to install the latest version of Heroku CLI for your platform in the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)


#### Virtual Environment

Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running the following code.

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages.

### Setup the database
* Start the postgres server

```
pg_ctl -D "C:\Program Files\PostgreSQL\14\data" start
```

* Create a postgresql database
1) Open the psql prompt and login.
2) Create a database  
example:

```
create database cinemadb;
```
* Set up environment variables.   
1) Update the database URL in the setup.sh  
Database URL format: 
``` 
DATABASE_URL={username}:{password}@{host}:{port}/{database_name}
```
example:
```
DATABASE_URL="postgresql://postgres:password@localhost:5432/cinemadb"
```
2) Run below two commands to set up environment variables:
```  bash
chmod +x setup.sh
source setup.sh
```
### Running the server
To run the server in the development mode use following commands:  
Linux environment:
``` bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Windows environment:
```cmd
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

Now you can access the API using http://127.0.0.1:5000/

### Setting up the authentication
To implement authorization and role based authentication you are adviced to use Auth0. Steps to setup Auth0 is given below:

1. Create a new [Auth0](https://auth0.com/) Account. 
2. Select a unique tenant domain. (ex: cinemaproject)
3. Create a new, single page web application (ex: Name:Cinema)
4. Create a new API (ex: Name:CinemaAPI, Identifier:cineapi, Signing Algorithm: RS256)
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token  
5. Update 'AUTH0_DOMAIN'(ex:cinemaproject.us.auth0.com), 'ALGORITHMS'(ex:RS256) and, 'API_AUDIENCE'(ex:cineapi) values in the setup.sh file. These values are used in the auth.py file.  
6. Create new API permissions: (API -> permissions tab)   
    -`get:movies`  
    -`get:actors`  
    -`post:movies`  
    -`post:actors`  
    -`patch:movies`  
    -`delete:movies`
7. Create new roles for: (User Management -> Roles) 
    - Casting Assistant      
        - can `get:movies`  
        - can `get:actors`  
    - Executive Producer  
        - can perform all actions
8. Register two users (User Management -> Users) in Auth0 account. Assign Casting Assistant and Executive Producer roles to each user.
9. Sign in to each account and make note of the JWT.
10. Update JWT token(obtained from the above step) values in the setup.sh for each role. These tokens are used in the test_app.py file for automated testing. 
11. API tests can run using the below command:
```
python test_app.py
```
12. You can use [Postman](https://www.postman.com/) to test API endpoints. (make sure to add the JWT token in the authorization tab)

### Deploying the web app in cloud
To deploy the above web app in cloud we use Heroku as the cloud platform. Steps to deploy the web app in cloud are as follows: (Assumption: Heroku CLI is already installed in your local machine)

1) login to heroku in the terminal  
```
heroku login -i
```
2) Run local db migrations  
    ```
    flask db init
    flask db migrate -m "Initial migration."
    ```
    This will create the migration folder in the folder structure and migration scripts inside versions folder.  
3) Initialize Git
```
git init
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```
4) Create an app in Heroku cloud
```
heroku create [my-app-name] --buildpack heroku/python
```
example:
```
heroku create imesha-fsnd-cinema --buildpack heroku/python
```
5) Check the Heroku dashboard in the browser and see that new application has created with the name that you have given in the above command(ex: imesha-fsnd-cinema). [Heroku dashboard](https://dashboard.heroku.com/apps)
6) Add PostgreSQL addon for our database
```
heroku addons:create heroku-postgresql:hobby-dev --app [my-app-name]
```
example:
```
heroku addons:create heroku-postgresql:hobby-dev --app imesha-fsnd-cinema
```
7) Configure the APP
* To get the DATABASE_URL run the below command:
```
heroku config --app [my-app-name]
```
example:
```
heroku config --app imesha-fsnd-cinema
```
* Copy the DATABASE_URL generated from the step above, and update your local DATABASE_URL environment variable using below command:
```
export DATABASE_URL="[DATABASE_URL-output from the above step]"
```
* Go to Heroku dashboard >> [Your APP] >> Settings >> Reveal Config Vars and add below variable names and their corresponding values.

| Config Vars | Example Values |  
| :---:       | :---:  |  
|ALGORITHMS   | ['RS256'] |
|API_AUDIENCE | cineapi |
|AUTH0_DOMAIN | cinemaproject.us.auth0.com |  
|DATABASE_URL | postgres://bazjwucweyadii:c0159...|
|EXCITED      | true |
|CASTING_ASSISTANT_JWT | Bearer eyJhbGciOiJSUzI1NiIsInR5cCI..|  
|EXECUTIVE_PRODUCER_JWT | Bearer eyJhbGciOiJSUzI1NiIsIn... | 
|            |               |  

8) Push the app to Heroku
* Commit the changes:
```
git add -A
git status
git commit -m "your message"
```
* Push the app to Heroku. This will trigger a heroku build automatically.
```
git push heroku main
```
* Migrate the database
```
heroku run python manage.py db upgrade --app [my-app-name]
```
example:
```
heroku run python manage.py db upgrade --app imesha-fsnd-cinema
```  
__Note: Each time when you make a change to your application you need to repeat this step__

9) Open the application from your Heroku Dashboard. Now you have a live application!
10) You can use [Postman](https://www.postman.com/) to test your live application. Application logs can view inside the heroku browser.


## API Reference

### Getting Started
- Base URL: https://imesha-fsnd-cinema.herokuapp.com/  
This API is up and running on the Heroku. 
- Authentication: 
    * If you are executing locally, as specified in the above section you need to obtain two JWT tokens for executive producer and casting assistant.
    * If you are using the Base URL specified above then you can use the JWT tokens specified below: (Same tokens are updated in the test_app.py)

    ```
    1) Executive Producer-  
    eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkEwTUZHWU0wakhoZmpDbDZnd3dGNSJ9.eyJpc3MiOiJodHRwczovL2NpbmVtYXByb2plY3QudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyNWNiYTZkNzBhMTgyMDA2OWQyYmM0ZCIsImF1ZCI6ImNpbmVhcGkiLCJpYXQiOjE2NTA4NjkzMzcsImV4cCI6MTY1MDk1NTczNywiYXpwIjoiWmJKRXZSZ0RabGNtNndDRFZONEtrc0lDMWJ1Sm1CazgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.uw_VWlW1PXJoeXVGT1fuBAHX_e-5NP1UokKyrXg0kwXI1ic2vEd6oUu5WrCJh2jRkZ3YhK8TvlS8tvDdsmFVgnijc_eCFDu_KuJKIg6wenm2sqviAkAROQwl8g6VptxQQ3_HxIzo2TH44923_AEb0gZKh1s-aM84sgBzyn_ThywnlfL8AoP9ticM_lW3cFzfA5xRzplMdsIfS4ByWMd83Vi8AgbmfT6fvDg7XFN85hj7DWNXThNAxv1x7rTpoezbTm1yZ7I0X2ZhsaxAhES_Q_E11OsjNIujWyzSh1jwLQGWrYl-NmLnAs9y0BysjGiTAomtvKIihONAbkwTawvOQw
    ```  

    ```
    2) Casting Assistant -  
    eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkEwTUZHWU0wakhoZmpDbDZnd3dGNSJ9.eyJpc3MiOiJodHRwczovL2NpbmVtYXByb2plY3QudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyNWNiOWUwN2QzOThkMDA2Zjk0NmFiNyIsImF1ZCI6ImNpbmVhcGkiLCJpYXQiOjE2NTA4Njk0NjQsImV4cCI6MTY1MDk1NTg2NCwiYXpwIjoiWmJKRXZSZ0RabGNtNndDRFZONEtrc0lDMWJ1Sm1CazgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.hB9SYZDwHwHTWFxbfUjhjq7jMmwg25t7TCRqiJMTMaBUddo8iCQ-cldTaDjLmRhaWALz2y2Vt0bji1UFtW_CtfVD_Xv-Ba1ffShypgTrJukgVzI08wUcrVpkk7fE1LPKFzaE9QkLwxEQ8_ijpeJfGmAjXy8E7hvdWal9C_OY4h3Vd95F72qUZtMiYECQg5g56uj0jMWQbEejuFh44jw0WDTOTDP3P2gaBZNuBBCupoTuV09RTxXAYNf4SijJYEQ50nBlubQufjPlFafkoZoG8vN1BpZ-baj-cdIQ92-L0cKZ21n4pckAfXhrZyoxnxrVM1S1O_Mh4MRoiBVJRxpDDA
    ```

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return following error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Method not allowed
- 500: Internal server error
- 403: forbidden
- 401: unauthorized

### Endpoints

#### GET '/'
- This is a public endpoint.
- This method is used to verify that the application is up and running successfully.
- Request Arguments: None
- Returns: An json object, that contains success value and a message-"Applicaion is up and running"

```
{
    "message":"Applicaion is up and running",
    "success":true
}
```

#### GET '/movies'
- This endpoint require the 'get:movies' permission.
- Fetches a dictionary of movies and success value.
- Request Arguments: None
- Returns: An json object, that contains success value and available all movies or appropriate status code indicating reason for failure.  

```
{
    "movies": [
        {
            "genre": "comedy",
            "id": 1,
            "name": "movie1"
        }
    ],
    "success": true
}
```

#### GET '/actors'
- This endpoint require the 'get:actors' permission.
- Fetches a dictionary of actors and success value.
- Request Arguments: None
- Returns: An json object, that contains success value and available all actors or appropriate status code indicating reason for failure.  

```
{
    "actors": [
        {
            "age": 25,
            "experience_level": "3",
            "gender": "female",
            "id": 1,
            "name": "Lisa"
        }
    ],
    "success": true
}
```

#### POST '/movies'
- This endpoint require the 'post:movies' permission.
- Creates a new movie in the movie table using the submitted json which includes name, and genre.
- Request Arguments: Request body,
```
{
    "name": "test movie",
    "genre": "horror"
}
```
- Returns: A json object which includes, a success value, and newly created movie details or appropriate status code indicating reason for failure.
```
{
    "movie": [
        {
            "genre": "horror",
            "id": 2,
            "name": "test movie"
        }
    ],
    "success": true
}
```

#### POST '/actors'
- This endpoint require the 'post:actors' permission.
- Creates a new actor in the actor table using the submitted json which includes name, experience level, gender and age.
- Request Arguments: Request body,
```
{
    "name": "Linda",
    "experience_level": "3",
    "gender":"female",
    "age":25
}
```
- Returns: A json object which includes, a success value, and newly created actor details or appropriate status code indicating reason for failure.
```
{
    "actor": [
        {
            "age": 25,
            "experience_level": "3",
            "gender": "female",
            "id": 2,
            "name": "Linda"
        }
    ],
    "success": true
}
```

#### PATCH '/movies/id'
- This endpoint require the 'patch:movies' permission.
- Updates a existing movie in the movie table using the submitted json which includes movie name, or the genre
- Request Arguments: Existing movie id(int, required, URL parameter)
                     Request body,
```
{
    "genre": "Romance"
}
```
- Returns: A json object which includes, a success value, and newly updated movie details or appropriate status code indicating reason for failure.

```
{
    "movie": [
        {
            "genre": "Romance",
            "id": 1,
            "name": "movie1"
        }
    ],
    "success": true
}
```

#### DELETE '/movies/id'
- This endpoint require the 'delete:movies' permission.
- Delete the row of the given movie id if it exists in the movie table.
- Request Arguments: movie id(int, required, URL parameter)
- Returns: A json object which includes, a success value, and id of the deleted record

```
{
    "deleted": 1,
    "success": true
}
```








