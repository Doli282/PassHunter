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

```shell
pip freeze > requirements.txt
```

## Database operations

```shell
# Database initialization
flask db init
# Database migration
flask db migrate -m "message  - migration changes"
# Database upgrade
flask db upgrade
# Database downgrade
flask db downgrade
```