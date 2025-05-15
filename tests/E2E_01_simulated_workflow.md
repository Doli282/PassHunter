# E2E_01_Simulated_workflow

This end-to-end test encompasses the whole workflow of the application,
from a user defining a watchlist on one end, data downloaded on the other end, and finally raising alerts.

## Preconditions

- operational modules
- interconnectivity between modules
- Telegram channel monitored by Forwarder
- prepared dataset (not previously uploaded to the application) with defined structure:
  - archive (may be protected by password - in that case, provide the password in the message)
  - files containing the credentials
    - the filename should include keywords like `password`
    - the file may, for example, look like this:
```text
SOFT: Chrome Default (131.0.6778.109)
URL: https://login.live.com/login.srf
USER: dummyuser
PASS: dummypassword

SOFT: Chrome Default (131.0.6778.109)
URL: https://accounts.autodesk.com/User/RegisterEducationUser
USER: dummyuser
PASS: dummypassword
```

## Steps

1. Create a user in the web application.
2. Create a watchlist and define a domain in the web GUI. Use a monitored string, that is (or is not) matched to the test data.
3. Set email alerts for the watchlist.
4. Upload the dataset to the monitored Telegram channel.

## Expected Result

1. Uploaded dataset is forwarded to a channel ownd by Monitor.
2. The dataset is downloaded and extracted.
3. Extracted files are uploaded to OpenSearch.
4. A domain from a watchlist is found and an alert is created.
5. The alert is visible in the web application.
6. An email is sent to the user-defined address.
