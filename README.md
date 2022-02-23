# Team Strategy Code Project

###### Shota Kameyama
###### Mathew Van Beek
###### Nils Linhoff
###### Mahamad Ibrahim
###### Muhammad Nasim Akbary

## Content:

### 1. Introduction
### 2. How to
#### 2.1 Purpose and Assumptions
#### 2.2 Prerequisites
#### 2.3 How to run Api
### 3. Discussion 
### 4. Appendix
#### 4.1 Test Scripts
### 5. References



## 1. Introduction

A large organization such as CERN (The European Organization for Nuclear Research) with its numerous laboratories and experiment equipment needs to have a well-organized and safe storage repository for maintenance reports.

## 2. How to

### 2.1 Purpose and Assumptions

The purpose of this repository is to provide secure access for qualified personal to maintenances reports of the CERN facility and its laboratories. The induvial reports can be viewed or edited if the user has the corresponding rights.

It is assumed that CERN, an organization with over 2500 employees (CERN, 2020), has several security policies implemented. The security policy should at least encompass GDPR (GDPR compliance checklist - GDPR.eu, no date) and OWASP (OWASP, 2021) recommendations. These should be among other things: pseudonymization of any real user data (e.g. numerical user ID), multi factor authentication, a strong password policy, encryption in transit and at rest, frequent employee training. 

### 2.2 Prerequisites


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

### 2.3 How to run API

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
http -f post http://127.0.0.1:5000/api/v1/report/upload Authentication-Token:GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE file@FILEPATH_THAT_YOU_WANT_UPLOAD name=REPORT_NAME description=REPORT_DESCRIPTION
```

### Download

[HTTPIE does not support a binary download](https://httpie.io/docs/cli/binary-data).

Use Curl and specify the name of the file.

```
curl -H "Authentication-Token:GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE" http://127.0.0.1:5000/api/v1/report/download/1 -o FILENAME_THAT_YOU_SPECIFY
```

If you do not specify the output file, then you will get the following warning message.

```
Warning: Binary output can mess up your terminal. Use "--output -" to tell 
Warning: curl to output it to your terminal anyway, or consider "--output 
Warning: <FILE>" to save to a file.
```



## 3. Discussion 

## 4. Appendix

### 4.1 Test Scripts

## 5. References

OWASP (2021) Top ten web application security risks. Available from: https://owasp.org/www-project-top-ten/ [Accessed February 1 2022]
GDPR compliance checklist - GDPR.eu (no date). Available from: https://gdpr.eu/checklist/ (Accessed: 18 October 2021).

