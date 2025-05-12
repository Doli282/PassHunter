# RabbitMQ

## Configuration

1. Create definitions in `definitions.json`
2. Set path to definitions in `rabbitmq.conf` configuration file.


### Generate password:

Passwords for the users can be generated either using the rabbitmq console or via API:
```shell
# CLI
rabbitmqctl hash_password mystrongpassword

# or
# API
curl -4su guest:guest -X GET localhost:15672/api/auth/hash_password/mystrongpassword
```

### Healthcheck:

To make sure the RabbitMQ instance has started successfully, use health check in the docker compose.

Documentation:
- author: Broadcom
- title: Monitoring
- subtitle Health checks
- medium: online
- year: 2025
- url: https://www.rabbitmq.com/docs/monitoring#health-checks
- date: 2025-05-06

# Disclaimer

Generative AI (ChatGPT) was used to create the `definitions.json` and `rabbitmq.conf`.

## ChatGPT

- author: OpenAI
- title: ChatGPT
- medium: software
- version: GPT-4.0
- year: 2025
- prompt: How to correctly configure the RabbitMQ? Create and include all files to run it in container with defined virtual hosts to divide the two queues (one queue per vhost). The confiuration should be prepared and set automatically. If possible, nothing should be configured manually
- url: https://chatgpt.com/share/682252e1-7d74-8004-bf4a-c753104501df
- date: 2025-04-28