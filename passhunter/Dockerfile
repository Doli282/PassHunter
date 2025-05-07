# pull official base image
FROM docker.io/library/python:3-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY passhunter/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY models /usr/src/app/app/models
RUN pip install /usr/src/app/app/models


# copy project
COPY passhunter /usr/src/app/

# Make entrypoint script executable
RUN chmod +x /usr/src/app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
