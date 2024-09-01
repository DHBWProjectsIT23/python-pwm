# Python Password Manager
- Entwickelt von Simon Blum, Ruth Fröhlich, Max Rodler.
## Example Data
By default there is no data within the database.
The script "scripts/populate_database.py" can be used to generate:
- User: "Test" - Password: "TestUser2103" - With a few passwords
- User: "Admin" - Password: "AdminUser2103" - Without passwords

Alternatively the files within import_export can be used to import
example data.
> Warning!
> Due to the complex encryption, the file "import_generated.json"
> Can take more then 45 seconds to import!

## Makefile
The Makefile contains commands for creating a venv and installing
all necessary dependencies.
Additionally it also contains commands for running pylint and mypy.

## Resizing and Terminal Size
The password manager resizes dynamically.
If the window is to small, a warning will be shown. The resizing can
feel sluggish if a lot of passwords are imported.
