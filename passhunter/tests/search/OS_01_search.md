# OS_01_Search

Try and test the search tool.

## Preconditions

_none_

## Steps

1. Go to `/search` - The search tool should be there.
2. Try searching for a couple of strings.
   - Examine what results are retrieved using wildcards (`*` and `?`) and what is retrieved without them.
   - e.g.: `*cvut.cz`, `vpn.*`, `*@gmail.com`, `faecbook.com`

## Expected Result

1. The search tool returns retrieved data - lines with queried string and name of the file in which it was found.
2. The number of all matches is displayed.
3. The results contain the searched term.
4. While globbing is used, the term can be only a substring of the matched words.
5. Using plain text returns only whole words.
