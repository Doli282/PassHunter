# SEC_01_Zip_bomb

Test what happens when a malicious archive containing a zip bomb is downloaded.

## Steps

1. Prepare a zip bomb.

Optional tool from GitHub:
title: zip-bomb
author: Damian Rusinek 
url: https://github.com/damianrusinek/zip-bomb
year: 2017
accessed: 2025-05-15

2. Extract the zip bomb using Extractor in a container

## Expected Result

The archive is extracted.
Zip bomb is being saved to the destination volume.
When the occupied size reaches the set limit, the container is restarted and the extracted zip bomb is removed.