"""
Lux_MySQLBackup

Copyright (c) 2024 LuxCoding

This script is licensed under the MIT License.
For full details, see the LICENSE file in the repository.
"""
# Import requiered Libs
import subprocess
import os
from datetime import datetime
from functions import load_config
from functions import load_language
from functions import translate
from functions import decrypt
from functions import encrypt_file
from functions import SQL

# Gets the curent Script Path and store it in a Variable
script_dir = os.path.dirname(__file__)

# Load Config and Translation
config = load_config()
translation = load_language(config.get('language'))

# Creates Backup Directory if its not exists
if not os.path.exists(config.get('backup_path')):
    os.makedirs(config.get('backup_path'))

# Function to cleanup old Backups
def cleanup_old_backups():
    backups = [f for f in os.listdir(config.get('backup_path')) if f.endswith('.sql')]
    backups.sort(key=lambda f: os.path.getmtime(os.path.join(config.get('backup_path'), f))) # Sort after last change time 

    # Check if there are more then allow count of backups
    if len(backups) > int(config.get('backup_count')):
        # get backups to delete
        old_backups = backups[:len(backups) - config.get('backup_count')]
        for backup in old_backups:
            os.remove(os.path.join(config.get('backup_path'), backup))
            print(translate('delete_old_backup_successfull', backup=backup))

# Funcstion to get all enabled Databases
def get_enabled_databases():
    databases = config.get('databases', {})
    if isinstance(databases, dict):
        return [db for db, enabled in databases.items() if enabled]
    return []  

# Get all Databases
databases = get_enabled_databases()

# Save every Database by its own
for db_name in databases:
    # Create Subfolder for every Database
    db_backup_dir = os.path.join(config.get('backup_path'), db_name)
    if not os.path.exists(db_backup_dir):
        os.makedirs(db_backup_dir)

    # Creates File name with current date
    current_time = datetime.now().strftime(config.get('date_format'))
    backup_filename = f"{db_name}_Backup_{current_time}.sql"
    backup_path = os.path.join(db_backup_dir, backup_filename)


    # Creates SQL file for every Database
    with open(backup_path, 'w', encoding='utf-8') as file:
        # CREATE DATABASE statement at the beginning of the file
        file.write(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\nUSE {db_name};\n\n")
        
        # Query all tables in the current database
        tables = SQL(db_name, "SHOW TABLES")

        for (table_name,) in tables:
            # CREATE TABLE statement for each table
            create_table_statement = SQL(db_name, f"SHOW CREATE TABLE {table_name}")

            file.write(create_table_statement[0][1] + ';\n\n')

            # SELECT * from each table to retrieve all data
            rows = SQL(db_name, f"SELECT * FROM {table_name}")

            # Create INSERT INTO statements for all rows of the table
            for row in rows:
                insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s' for _ in row])});"
                file.write(insert_query % tuple(row) + '\n')

            # Blank line between tables for better readability
            file.write("\n")

        print(f"Export für {db_name} abgeschlossen.")
    
    if config.get('use_encryption') and decrypt(config.get('encryption_password')) != "":
        encrypt_file(backup_path, backup_path, decrypt(config.get('encryption_password')))