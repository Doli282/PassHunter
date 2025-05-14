FROM docker.io/library/python:3-slim

# Install gosu according to https://github.com/tianon/gosu/blob/master/INSTALL.md
RUN set -eux; \
	apt-get update; \
	apt-get install -y gosu; \
	rm -rf /var/lib/apt/lists/*; \
# verify that the binary works
	gosu nobody true

# Create a non-root user
RUN groupadd -g 1221 huntergroup && \
    useradd -m -u 1221 -g huntergroup hunter

WORKDIR /app

COPY ./monitor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY models ./models
RUN chown -R hunter:huntergroup /app
RUN pip install ./models

COPY monitor .

RUN chown -R hunter:huntergroup /app && \
    chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
