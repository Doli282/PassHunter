FROM docker.io/opensearchproject/opensearch:latest

# Switch context according to official Dockerfile
WORKDIR /usr/share/opensearch
USER opensearch

# Install plugin
RUN /usr/share/opensearch/bin/opensearch-plugin install --batch ingest-attachment

# Run Opensearch
ENTRYPOINT ["./opensearch-docker-entrypoint.sh"]
CMD ["opensearch"]