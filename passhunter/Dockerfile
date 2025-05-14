# pull official base image
FROM docker.io/library/python:3-slim

# set work directory
WORKDIR /usr/src/passhunter

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY passhunter/requirements.txt /usr/src/passhunter/requirements.txt
RUN pip install -r requirements.txt

COPY models /usr/src/passhunter/app/models
RUN pip install /usr/src/passhunter/app/models


# copy project
COPY passhunter /usr/src/passhunter/

# Make entrypoint script executable
RUN chmod +x /usr/src/passhunter/entrypoint.sh
RUN chmod +x /usr/src/passhunter/db_init.sh

# Set entrypoint
ENTRYPOINT ["/usr/src/passhunter/entrypoint.sh"]
