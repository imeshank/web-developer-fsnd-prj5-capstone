# Casting Agency Project

## Introduction
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. This application includes,  
1) Two db models: Movie and Actor
2) API includes 6 endpoints  
3) Two job roles(Casting Assistant and Executive Producer) can access the API and each role has different permissions.  

## Getting Started - Running project locally

* Clone the repository to local machine.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Postgres 14.2

Follow instructions to install the latest version of postgres for your platform in the [postgresql](https://www.postgresql.org/download/)


#### Virtual Environment

Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running the following code.

```bash
pip install -r requirements.txt
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
1) Update the database URL in the setup.sh.
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

``` bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Now you can access the API using http://127.0.0.1:5000/

### Setting up the authentication
To implement authorization and role based authentication you are adviced to use Auth0. Steps to setup Auth0 is given below:

1. Create a new Auth0 Account. [Auth0](https://auth0.com/)
2. Select a unique tenant domain. (ex: cinemaproject)
3. Create a new, single page web application (ex: Name:Cinema)
4. Create a new API (ex: Name:CinemaAPI, Identifier:cineapi, Signing Algorithm: RS256)
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token  
5. Update 'AUTH0_DOMAIN'(ex:cinemaproject.us.auth0.com), 'ALGORITHMS'(ex:RS256) and, 'API_AUDIENCE'(ex:cineapi) values in the auth.py file.  
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
10. Update JWT token(obtained from the above step) values in the test_app.py for each role. 
11. API tests can run using the below command:
```
python test_app.py
```
12. You can use [Postman](https://www.postman.com/) to test API endpoints. (make sure to add the JWT token in the authorization tab)

## API Reference

### Getting Started
- Base URL: 


