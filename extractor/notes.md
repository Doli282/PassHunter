# Commands

Dependencies:

```shell
apt install unrar
apt install p7zip-full
apt install file # For detecting the file type
```

```shell
pip install patool
pip install celery
pip install python-dotenv
```

## Extraction

There are two approaches to how to address extraction.
Either to have a separate function for different archive formats
or to use some general tool that can distinguish the formats and choose the best tool by itself.
Secondly, it is more efficient to extract only the important files  
instead of extracting the whole archive and then pick only the valuable files.

https://rarfile.readthedocs.io/index.html
https://docs.python.org/3/library/zipfile.html#module-zipfile

Using separate functions for different archive formats would utilize libraries like ZipFile and RarFile.
The benefits are more efficient use of the library's features and possible customization of individual functions.
However, they also have their limitations.
ZipFile and RarFile enable extracting only specific files.
An extension for other formats means adding another function and another library.
Moreover, ZipFile does not support AES encryption.
Thus, despite having the .zip extension, the archive cannot be extracted.
It knows the directory structure of the archive content, but it is unable to extract the individual files due to an unknown format.
Hence, this method was deemed unsufficient, since AES-encrypted archives are quite prevalent. 

Snippet showing a function selecting only intended files to extract:
```python
# Open the zip archive
with zipfile.ZipFile(archive_path, 'r') as zip_ref:
    # Iteration variable for naming
    i = 1
    # Read information on all files and filter only desired files
    for file in zip_ref.infolist():
        if _filename_filter(file.filename):
            # Extract the file
            zip_ref.extract(file, extract_to_dir, bytes(archive_password, 'utf-8') if archive_password else None)
            i += 1
```

The second approach is to use a tool that can find the most appropriate tool for the extraction by itself.
Thanks to this, only a single function is necessary to invoke the extraction.
On the other hand, these general tools offer only general API functions that are supported by all tools discarding specific features of individual tools.
Consequently, it is mandatory to first extract the whole archive and then find the relevant files.
This can lead to a slower performance and higher space usage.

The general tool used in the application is `patool`.
This tool relies on external tools.
(Although the same applies for RarFile, too.)
However, it is also capable of identifying and extracting AES-encrypted archives.
https://github.com/wummel/patool
https://wummel.github.io/patool/
