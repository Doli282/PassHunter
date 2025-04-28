FROM docker.io/library/python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["celery","-A","extractor","worker","--loglevel=info","--queues=downloads"]
