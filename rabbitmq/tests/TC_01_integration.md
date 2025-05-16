# TC_01_Integration

Test the integration to other modules.
Test the producer-consumer communication.

## Preconditions

Working services Downloader, Extractor, Monitor.

## Steps

Run the services and monitor that the producer sends a task to the queue and a consumer accepts the task.
There are two producer-consumer pairs:
1. Downloader - Extractor
2. Extractor - Monitor

Use the console on http://localhost:15672/ for debugging and monitoring.

## Expected Result

The pair Downloader - Extractor:
- Downloader sends a task to the 'downloads' queue.
- Extractor receives the task.

The pair Extractor - Monitor:
- Extractor sends a task to the 'downloads' queue.
- Monitor receives the task.
