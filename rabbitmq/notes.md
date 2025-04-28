# RabbitMQ

## Configuration

1. Create definitions in `definitions.json`
2. Set path to definitions in `rabbitmq.conf` configuration file.


Generate password:
```shell
# CLI
rabbitmqctl hash_password foobarbaz

# API
curl -4su guest:guest -X GET localhost:15672/api/auth/hash_password/foobarbaz
```