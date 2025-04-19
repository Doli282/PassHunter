# Database

## Models and relations

Models are defined as follows:
- Account
- Watchlist
- Domain
- Alert

Accounts are used for authentication and authorization.
Anyone who wants to use the application creates can register an account.
An account is identified by artificial ID.
Its natural identifier is an email address.
Password must be set up for an account.
Only the hash is stored in the database.
Hash is created by library function using the `scrypt` hash function
**TODO citace**
https://datatracker.ietf.org/doc/html/rfc7914.html
https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.security.generate_password_hash
The account defines their own space.

A user can create and manage watchlists.
There can be many watchlists for one account.
A watchlist is private and exists only in the account's space.
It is defined by artificial ID.
When a user account is deleted, their watchlists are deleted as well.
A watchlist is a list of monitored domains.
There may be many domains added to one watchlist.

Domains denote registered domains for monitoring.
One domain can be present in many watchlists.
Domains are shared and each domain is defined only once in the database to save resources.
Same domains are not repeated and occupy only one row in the table.
More importantly, searches are not repeated during monitoring. 
A domain instance in the database can be created by any user.
There is no lookup tool to query defined domains.
Thus, other users do not know which domains are defined in the database.
A domain record gets deleted, once it is not contained in any watchlist.

If a domain is found in a new batch of data, an alert is raised.
Hence it is inherently connected to domains.
Alert is also connected to watchlists.
This connection defines for which watchlist the alert was raised.
This enables to calculate the efficiency of the watchlist -- how many alerts it has raised.
Consequently, if a user monitors one domain in many watchlists, alerts are raised for the domain by all watchlists.
If either a watchlist or the monitored domain is deleted from the database, the alert is deleted, too.
The reason for this operation is to clean alerts that cannot be linked to any domain or watchlist that raised that alert.

