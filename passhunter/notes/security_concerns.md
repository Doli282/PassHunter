# Security consideration

## URL redirects

### Login page - mitigated

The application supports redirects to previously asked resource if login was invoked as a result of an attempt to access resource requiring authentication.
The redirect URL must not contain domain name.
It must be a relative path.

This prevents URL Redirects attacks.
On the other hand, it does not allow redirects to other hosts.
However, the application does not use this feature anywhere.

## Enumeration

### Registration page - accepted

The registration page enables enumeration of email addresses of registered accounts.
There is a warning message when a new user wants to register with an email address that is already taken.
The warning indicates the email address is in use and the user should choose another one.

This vulnerability is known and accepted.
Users must be informed that the registration is not possible.
Telling them the reason why the registration failed allows them to make a correct attempt.
