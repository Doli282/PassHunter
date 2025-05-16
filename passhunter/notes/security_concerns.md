# Security consideration

## URL redirects

### Login page - mitigated

The application supports redirects to a previously requested resource if login was invoked as a result of an attempt to access resource requiring authentication.
The redirect URL must not contain a domain name.
It must be a relative path.

This prevents URL Redirects attacks.
On the other hand, it does not allow redirects to other hosts.
However, the application does not use this feature anywhere.

## Access to others' watchlists

Requests for retrieving objects from the database implicitly use the ID of the current user.
Hence, each user can access only objects that are related to their account.

## Enumeration

### Registration page -- accepted

The registration page enables enumeration of email addresses of registered accounts.
There is a warning message when a new user wants to register with an email address that is already taken.
The warning indicates the email address is in use and the user should choose another one.

This vulnerability is known and accepted.
Users must be informed that the registration is not possible.
Telling them the reason why the registration failed allows them to make a correct attempt.

### Existing watchlists -- mitigated

The access to a watchlist belonging to another user returns '404 Not Found' error instead of '403 Forbidden', even though the object exists.
Therefore, it is not possible to enumerate which IDs are used.


## JavaScript

### MomentJS

JavaScript is used for a momentjs library for rendering local time.
When JS is disabled, UTC time is displayed.
