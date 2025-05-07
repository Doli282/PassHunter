FROM docker.io/library/python:3-slim
WORKDIR /app
COPY monitor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ../models ./models
RUN pip install ./models
COPY monitor .
ENTRYPOINT ["celery","-A","uploader","worker","--loglevel=info","--queues=uploads"]
