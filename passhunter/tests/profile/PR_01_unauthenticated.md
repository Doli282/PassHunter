# PR_01_Unauthenticated

Explore the application as an unauthenticated user.

## Preconditions

_none_

## Steps

1. Explore various endpoints an unauthenticated user can access. Especially try:
   1. `/index` - homepage
   2. `/search` - search tool - Try using the tool.
   3. `/login` - login page
   4. `/register` - registration form
   5. `/domains` - domains
   6. `/watchlsits` - watchlsits
   7. `/alerts` - alerts


## Expected Result

An unauthenticated user is supposed to have access to following pages:
    1. `/index` - homepage
   2. `/search` - search tool - Try using the tool.
   3. `/login` - login page
   4. `/register` - registration form

Other pages should be forbidden.
When an anonymous user tries to access a forbidden resource, he is to be redirected to the login page.
