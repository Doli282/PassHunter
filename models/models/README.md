# Models package

Defines models used in the PassHunter application.
Install as a package into modules that access the database.

## Models

The following models are defined:
- account
- alert
- domain
- file
- watchlist

## Installation

Local installation for testing and development:
```shell
pip install -e models
```

Installation in the docker containers:
```dockerfile
# Example
COPY ../models /usr/src/app/app/models
RUN pip install /usr/src/app/app/models
```