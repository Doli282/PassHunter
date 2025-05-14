FROM docker.io/library/python:3-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Create a non-root user
RUN groupadd -g 1221 huntergroup && \
    useradd -m -u 1221 -g huntergroup hunter && \
    chown -R hunter:huntergroup /app
USER hunter

ENTRYPOINT ["python", "-u", "forwarder.py"]
