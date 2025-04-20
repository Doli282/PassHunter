# Email services

## Logging errors with emails to admins

### Test

Run a fake mail service.
It will print the to-be-sent message.


Set environment variables:
```shell
# .env
# Mail server - error reporting
MAIL_SERVER=localhost
MAIL_PORT=8025
#MAIL_USE_TLS=
#MAIL_USERNAME=
#MAIL_PASSWORD=
```
```shell
# .flaskenv
FLASK_DEBUG=0
```

Run in another shell:
```shell
python3 -m venv venv-mailserver
source venv-mailserver/bin/activate

# Run a dummy mail service
pip install aiosmtpd
aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025
```

