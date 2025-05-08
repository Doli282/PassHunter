FROM docker.io/library/python:3-slim

WORKDIR /app

COPY ./monitor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY models ./models
RUN pip install ./models


COPY monitor .
#COPY monitor/opensearch/ monitor/config.py monitor/database.py monitor/monitor.py  ./

#ENTRYPOINT ["python", "-u", "monitor.py"]
ENTRYPOINT ["celery","-A","monitor","worker","--loglevel=info","--queues=uploads"]
