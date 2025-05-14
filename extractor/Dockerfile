FROM docker.io/library/python:3-slim

WORKDIR /app

# Enable contrib and non-free repositories
RUN sed -i 's/Components: main/Components: main contrib non-free/' /etc/apt/sources.list.d/debian.sources

# Install gosu according to https://github.com/tianon/gosu/blob/master/INSTALL.md
# Update package lists and install unrar and other tools
RUN apt-get update && \
    apt-get install -y file unrar p7zip-full && \
    apt-get install -y gosu && \
    rm -rf /var/lib/apt/lists/*; \
# verify that the binary works
	gosu nobody true

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source files
COPY . .

# Create a non-root user
RUN groupadd -g 1221 huntergroup && \
    useradd -m -u 1221 -g huntergroup hunter && \
    chown -R hunter:huntergroup /app && \
    chmod +x ./entrypoint.sh

# Launch Celery worker
ENTRYPOINT ["./entrypoint.sh"]
