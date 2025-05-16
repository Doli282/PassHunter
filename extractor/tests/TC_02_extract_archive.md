# TC_01_Extract_archive

Test extracting archives.

## Dependencies

The 'filter file' feature is dependent on the test `01_File_filter`

## Preconditions

- Prepare archives for the testing.
Archives may be of different formats: .zip, .rar, .7z, .tar, ...
Archives may or may not use passwords for encrypting the archive.
- Prepare directories:
  - input directory for the archives
  - output directory for the extracted files

## Steps

1. Prepare the test archives for different scenarios according to preconditions.
2. Launch the script to extract the archives. Make sure they are in the correct directories.


## Expected Result

1. The archive is extracted. Extracted files are in the specified destination directory.
2. Only files chosen by the filter function (e.g., containing keywords) are in the destination directory.
3. The original archive is removed.
