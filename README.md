
Build environment
```
python3 -m venv pymyenv
. pymyenv/bin/activate
make install
```

Set Env Variables

```
export FLASK_APP="app.py"
python -c 'import secrets; print(secrets.token_urlsafe())'
export SECRET_KEY="YourSecrets"
python -c 'import secrets; print(secrets.SystemRandom().getrandbits(128))'
export SECURITY_PASSWORD_SALT="YourSalt"
export DATABASE_USER="YourDatabaseUserName"
export DATABASE_PASSWORD="YourDatabasePassword"
export DATABASE_HOST="YourDatabaseHost"
export DATABASE_NAME="YourDatabaseName"
export -p
```


You need to run make check and pass all the detected errors before you commit

```
make check
```

# How to run API

One Terminal
```
flask run
```

A different Terminal Run the following as per method you want.

## Auth Microservice

### Register

Curl Request:

```
curl -H "Content-Type: application/json" --data '{"username":"example_name","password":"example_password", "email":"example@example.com"}' http://127.0.0.1:5000/api/v1/auth/register
```

HTTPIE Request:

```
 http POST http://127.0.0.1:5000/api/v1/auth/register email='example@example.com' password='example_password'
```


### Login

Curl Request:

```
curl -H "Content-Type: application/json" --data '{"username":"example_name","password":"example_password", "email":"example@example.com"}' http://127.0.0.1:5000/api/v1/auth/login
```

HTTPIE Request: 

```
 http POST http://127.0.0.1:5000/api/v1/auth/login email='example@example.com' password='example_password'
```

### Index

You need to get auth_token with Login API!

HTTPIE Request:

```
 http GET http://127.0.0.1:5000/api/v1/auth/index auth_token=GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE
```


## Report Microservice

You need to get auth_token with Login API!

### List

HTTPIE Request:

```
 http GET http://127.0.0.1:5000/api/v1/report/list auth_token=GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE
```

### Upload (Create)

HTTPIE Request:

```
http -f post http://127.0.0.1:5000/api/v1/report/upload Authentication-Token:GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE file@FILEPATH_THAT_YOU_WANT_UPLOAD
```


