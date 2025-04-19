# Database

## Installed libraries
```shell
pip install --upgrade pip
pip install email-validator
pip install flask
pip install flask-login
pip install flask-migrate
pip install flask-sqlalchemy
pip install flask-wtf
pip install psycopg2-binary
pip install python-dotenv
#pip install sqlalchemy-utils
```


## Database operations

Database initialization
```shell
flask db init
```

Database migration
```shell
flask db migrate -m "message  - migration chagnes"
```

Database upgrade
```shell
flask db upgrade
```

Database downgrade
```shell
flask db downgrade
```