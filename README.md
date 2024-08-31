# Python Password Manager
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
