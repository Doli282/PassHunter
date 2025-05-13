# 01_SEC_unauthorized_access

Accessing resources of other users has to be forbidden.
Only authorized access (by the owner of the resource) must be permitted.

## Preconditions

- 2 different users defined (user A, user B)
- defined resources (watchlists, domains, alerts) for user B

## Steps

1. Log as user B.
2. Identify IDs (integer in the URL) for resources owned by user B.
3. Log as user A.
4. Access resources of user B. (Use the IDs in URL.)

## Expected Result

1. The access is forbidden.
2. The response from the server is 404 Not Found.
