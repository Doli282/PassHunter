# TC_01_File_filter

Test filtering files.
The filter checks filenames against a list of keywords

## Preconditions

1. A list of keywords defined for the filtering. E.g.:
    - ['pass']
2. A list of filenames. E.g.:
   - ['All Passwords.txt', 'passwords.txt', 'history.txt', 'processes.txt', 'image.jpg', 'passport.pdf', 'users.md']
   

## Steps

1. Prepare a list of keywords and filenames as mentioned in the preconditions.
2. Filter the filenames based on the keywords.

## Expected Result

Filenames containing the keywords return true, while other filenames return false.
E.g., these filenames return true:
- ['All Passwords.txt', 'passwords.txt', 'passport.pdf']
