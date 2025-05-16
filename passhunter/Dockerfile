FROM docker.io/library/python:3-slim

# Create a non-root user
RUN groupadd -g 1221 huntergroup && \
    useradd -m -u 1221 -g huntergroup hunter

# set work directory
WORKDIR /usr/src/passhunter

# copy project
COPY models /usr/src/passhunter/app/models
COPY passhunter /usr/src/passhunter/

# Make entrypoint script executable
RUN chown -R hunter:huntergroup /usr/src/passhunter
RUN chmod +x /usr/src/passhunter/entrypoint.sh
RUN chmod +x /usr/src/passhunter/db_init.sh
USER hunter

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --no-cache-dir --upgrade pip --user
RUN pip install --no-cache-dir -r requirements.txt --user
RUN pip install /usr/src/passhunter/app/models --user

# Set entrypoint
ENTRYPOINT ["/usr/src/passhunter/entrypoint.sh"]
