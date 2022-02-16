
Build environment
```
python3 -m venv pymyenv
. pymyenv/bin/activate
make install
export FLASK_APP="app.py"
<!-- export FLASK_DEBUG=1 -->
<!-- python -c 'import secrets; print(secrets.token_hex())' -->
python -c 'import secrets; print(secrets.token_urlsafe())'
export SECRET_KEY="YourSecrets"
python -c 'import secrets; print(secrets.SystemRandom().getrandbits(128))'
export SECURITY_PASSWORD_SALT="YourSalt"
export -p
```

Test
```
make test
```

Lint
```
make lint
```