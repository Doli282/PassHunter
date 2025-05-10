FROM docker.io/library/python:3-slim

WORKDIR /app

# Enable contrib and non-free repositories
RUN sed -i 's/Components: main/Components: main contrib non-free/' /etc/apt/sources.list.d/debian.sources

# Update package lists and install unrar
RUN apt-get update && \
    apt-get install -y unrar p7zip-full && \
    rm -rf /var/lib/apt/lists/*

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source files
COPY . .

# Launch Celery worker
ENTRYPOINT ["celery","-A","extractor","worker","--loglevel=info","--queues=downloads"]
