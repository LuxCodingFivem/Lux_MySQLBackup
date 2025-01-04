"""
My Python Script

Copyright (c) 2024 LuxCoding

This script is licensed under the MIT License.
For full details, see the LICENSE file in the repository.
"""
# Import requiered Libs
import subprocess
import os
from datetime import datetime

# Config
# Create the Translation 
locale = 'en'

# Date format (%d = Day, %m = Month, %Y = Year, %H = Hour, %M = Minute, %S = Seconed)
date_format = '%d.%m.%Y_%H.%M.%S'

translation = {
    'de': {
        'error_by_get_database': 'Fehler beim Abrufen der Datenbanken: {utf8}',
        'delete_old_backup': 'Altes Backup gelöscht: {backup}',
        'database_skiped': 'Datenbank {db_name} wird übersprungen.',
        'backup_success': 'Backup erfolgreich für Datenbank {db_name}: {backup_path}',
        'backup_failed': 'Backup fehlgeschlagen für Datenbank {db_name}: {utf8}',
    },
    'en': {
        'error_by_get_database': 'Error retrieving databases: {utf8}',
        'delete_old_backup': 'Old backup deleted: {backup}',
        'database_skiped': 'Database {db_name} is skipped.',
        'backup_success': 'Backup successful for database {db_name}: {backup_path}',
        'backup_failed': 'Backup failed for database {db_name}: {utf8}',
    },
    'sp': {
        'error_by_get_database': 'Error al recuperar las bases de datos: {utf8}',
        'delete_old_backup': 'Copia de seguridad antigua eliminada: {backup}',
        'database_skiped': 'Se omite la base de datos {db_name}.',
        'backup_success': 'Copia de seguridad exitosa para la base de datos {db_name}: {backup_path}',
        'backup_failed': 'Error en la copia de seguridad de la base de datos {db_name}: {utf8}',
    },
    'fr': {
        'error_by_get_database': 'Erreur lors de la récupération des bases de données : {utf8}',
        'delete_old_backup': 'Ancienne sauvegarde supprimée : {backup}',
        'database_skiped': 'La base de données {db_name} est ignorée.',
        'backup_success': 'Sauvegarde réussie pour la base de données {db_name} : {backup_path}',
        'backup_failed': 'Échec de la sauvegarde pour la base de données {db_name} : {utf8}',
    },
    'it': {
        'error_by_get_database': 'Errore durante il recupero dei database: {utf8}',
        'delete_old_backup': 'Vecchio backup eliminato: {backup}',
        'database_skiped': 'Database {db_name} saltato.',
        'backup_success': 'Backup riuscito per il database {db_name}: {backup_path}',
        'backup_failed': 'Backup fallito per il database {db_name}: {utf8}',
    },
    'pt': {
        'error_by_get_database': 'Erro ao recuperar os bancos de dados: {utf8}',
        'delete_old_backup': 'Backup antigo excluído: {backup}',
        'database_skiped': 'Banco de dados {db_name} foi pulado.',
        'backup_success': 'Backup bem-sucedido para o banco de dados {db_name}: {backup_path}',
        'backup_failed': 'Falha no backup do banco de dados {db_name}: {utf8}',
    },
    'zh': {
        'error_by_get_database': '检索数据库时出错：{utf8}',
        'delete_old_backup': '已删除旧备份：{backup}',
        'database_skiped': '数据库 {db_name} 被跳过。',
        'backup_success': '数据库 {db_name} 的备份成功：{backup_path}',
        'backup_failed': '数据库 {db_name} 的备份失败：{utf8}',
    },
    'ja': {
        'error_by_get_database': 'データベースの取得中にエラーが発生しました: {utf8}',
        'delete_old_backup': '古いバックアップを削除しました: {backup}',
        'database_skiped': 'データベース {db_name} はスキップされました。',
        'backup_success': 'データベース {db_name} のバックアップが成功しました: {backup_path}',
        'backup_failed': 'データベース {db_name} のバックアップに失敗しました: {utf8}',
    },
    'ru': {
        'error_by_get_database': 'Ошибка при получении баз данных: {utf8}',
        'delete_old_backup': 'Старый бэкап удалён: {backup}',
        'database_skiped': 'База данных {db_name} пропущена.',
        'backup_success': 'Резервное копирование базы данных {db_name} выполнено успешно: {backup_path}',
        'backup_failed': 'Ошибка резервного копирования базы данных {db_name}: {utf8}',
    },
    'tr': {
        'error_by_get_database': 'Veritabanları alınırken hata oluştu: {utf8}',
        'delete_old_backup': 'Eski yedekleme silindi: {backup}',
        'database_skiped': 'Veritabanı {db_name} atlandı.',
        'backup_success': 'Veritabanı {db_name} için yedekleme başarılı: {backup_path}',
        'backup_failed': 'Veritabanı {db_name} için yedekleme başarısız: {utf8}',
    },
    'nl': {
        'error_by_get_database': 'Fout bij het ophalen van databases: {utf8}',
        'delete_old_backup': 'Oude back-up verwijderd: {backup}',
        'database_skiped': 'Database {db_name} wordt overgeslagen.',
        'backup_success': 'Back-up geslaagd voor database {db_name}: {backup_path}',
        'backup_failed': 'Back-up mislukt voor database {db_name}: {utf8}',
    }
}

# function to translate 
def translate(key, **kwargs):
    text = translation.get(locale, {}).get(key, key)  
    try:
        return text.format(**kwargs) 
    except KeyError:
        return text


# Defining Variables for the mySQL Connection
db_host = 'localhost'  # Hostname or IP of the Database
db_user = ''  # Database Username
db_password = ''  # Database Password

# Defining Variables for Backup 
backup_base_dir = 'C:/Users/Administrator/OneDrive/MySQL Backups'  # Where sould the Backup be stored 
versionen_behalten = 360 # how many Backups sould be saved until the Backups will deleted 

# Path to mysql.exe and mysqldump.exe
mysql_path = 'C:/Program Files/MariaDB 11.5/bin/mysql.exe'
mysqldump_path = 'C:/Program Files/MariaDB 11.5/bin/mysqldump.exe'

# Exclude Databases
exclude_databases = ['information_schema', 'performance_schema', 'sys', 'mysql']

# Create The Backup Director if its not exists 
if not os.path.exists(backup_base_dir):
    os.makedirs(backup_base_dir)

# Funcstion to get all Databases
def get_databases():
    cmd = [
        mysql_path,  
        '-h', db_host,
        '-u', db_user,
        f'--password={db_password}',
        '-e', 'SHOW DATABASES;'
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(translate('error_by_get_database', utf8=result.stderr.decode('utf-8')))
        return []
    
    databases = result.stdout.decode('utf-8').splitlines()[1:]  # Ignore the Headline
    return databases

# function to delete the old backups
def cleanup_old_backups(db_backup_dir):
    backups = [f for f in os.listdir(db_backup_dir) if f.endswith('.sql')]
    backups.sort(key=lambda f: os.path.getmtime(os.path.join(db_backup_dir, f)))  # sort by Edit time

    # Check if there is more Backups the defined 
    if len(backups) > versionen_behalten:
        # Calculate Backups to delete
        old_backups = backups[:len(backups) - versionen_behalten]
        for backup in old_backups:
            os.remove(os.path.join(db_backup_dir, backup))
            print(translate('delete_old_backup', backup=backup))

# Get Databesed
databases = get_databases()

# Backup the databases individually except the excluded ones
for db_name in databases:
    if db_name in exclude_databases:
        print('database_skiped', db_name=db_name)
        continue

    # Create Subfolder for every Databse
    db_backup_dir = os.path.join(backup_base_dir, db_name)
    if not os.path.exists(db_backup_dir):
        os.makedirs(db_backup_dir)
    
    # Create an file name with current time stemp
    current_time = datetime.now().strftime(date_format)
    backup_filename = f"{db_name}_backup_{current_time}.sql"
    backup_path = os.path.join(db_backup_dir, backup_filename)
    
    # mysqldump-command to save the Databases 
    dump_cmd = [
        mysqldump_path,
        '-h', db_host,
        '-u', db_user,
        f'--password={db_password}',
        db_name
    ]
    
    # Start the Backup and wirte it in the files
    with open(backup_path, 'w') as f:
        result = subprocess.run(dump_cmd, stdout=f, stderr=subprocess.PIPE)
    
    # Check for errors
    if result.returncode == 0:
        print(translate('backup_success', db_name=db_name, backup_path=backup_path))
    else:
        print(translate('backup_failed', db_name=db_name, utf8=result.stderr.decode('utf-8')))
    
    # Delete old Backups
    cleanup_old_backups(db_backup_dir)