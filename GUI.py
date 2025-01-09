"""
Lux_MySQLBackup GUI

Copyright (c) 2024 LuxCoding

This script is licensed under the MIT License.
For full details, see the LICENSE file in the repository.
"""
# Import requiered Libs
import os
import subprocess
import sys
import customtkinter 
import tkinter
from tkinter import filedialog
from py.functions import encrypt
from py.functions import decrypt
from py.functions import load_config
from py.functions import load_language
from py.functions import translate
from py.functions import save_config
from py.functions import get_databases

checkbox_vars = {}

# Gets the curent Script Path and store it in a Variable
script_dir = os.path.dirname(__file__)

# Function to Restart GUI
def restart_GUI():
    app.destroy()
    subprocess.Popen([sys.executable, os.path.join(script_dir, 'GUI.py')])

# Function to save Configuration to Config File
def save_settings():
    # General Settings
    config['language'] = language_dropdown_field.get()
    config['date_format'] = date_format.get()
    config['backup_path'] = backup_dir_entry.get()
    config['backup_count'] = backup_count_entry.get()
    config['mysql_exe_path'] = mysql_exe_entry.get()
    config['mysql_dump_exe_path'] = mysql_dump_exe_entry.get()

    # Database Connection
    config['database_user'] = encrypt(database_user_entry.get())
    config['database_password'] = encrypt(database_password_entry.get())
    config['hostname'] = encrypt(hostname_entry.get())

    # Databases
    config['databases'] = {}
    for db, var in checkbox_vars.items():
        config['databases'][db] = var.get()

    # Encryption
    config['use_encryption'] = use_encryption_checkbox_var.get()
    config['encryption_password'] = encrypt(encryption_password_entry.get())

    # Theme
    config['background_theme'] = background_theme_dropdown.get()
    config['theme_color'] = theme_color_dropdown.get()

    # Save Config
    save_config(config) 
    
    # Restart GUI
    restart_GUI()


# Function to fill in values to Entrys from Settings
def fill_in_values():
    # General Settings 
    date_format.delete(0, customtkinter.END)
    date_format.insert(0, config.get('date_format'))

    backup_dir_entry.delete(0, customtkinter.END)
    backup_dir_entry.insert(0, config.get('backup_path'))

    backup_count_entry.delete(0, customtkinter.END)
    backup_count_entry.insert(0, config.get('backup_count'))

    mysql_exe_entry.delete(0, customtkinter.END)
    mysql_exe_entry.insert(0, config.get('mysql_exe_path'))

    mysql_dump_exe_entry.delete(0, customtkinter.END)
    mysql_dump_exe_entry.insert(0, config.get('mysql_dump_exe_path'))

    # Database Connection
    hostname_entry.delete(0, customtkinter.END)
    hostname_entry.insert(0, decrypt(config.get('hostname')))

    database_user_entry.delete(0, customtkinter.END)
    database_user_entry.insert(0, decrypt(config.get('database_user')))

    database_password_entry.delete(0, customtkinter.END)
    database_password_entry.insert(0, decrypt(config.get('database_password')))

    # Databases
    for db, value in config['databases'].items():
        if db in checkbox_vars: 
            checkbox_vars[db].set(value) 

    # Encryption
    use_encryption_checkbox_var.set(config.get('use_encryption'))
    
    encryption_password_entry.delete(0, customtkinter.END)
    encryption_password_entry.insert(0, decrypt(config.get('encryption_password')))

# Function to Select the backup Path
def select_backup_dir():
    path = filedialog.askdirectory(initialdir="/", title=translate('choose_backup_dir')) 
    backup_dir_entry.delete(0, customtkinter.END)
    backup_dir_entry.insert(0, path)

# Function to Select the MySQL.exe Path
def select_mysql_exe_dir():
    path = filedialog.askopenfilename(initialdir="/", title=translate('choose_mysql_exe_dir'), filetypes=(("exe files", "*.exe"),("all files", "*.*"))) 
    mysql_exe_entry.delete(0, customtkinter.END)
    mysql_exe_entry.insert(0, path)

# Function to Select the MySQLDump.exe Path
def select_mysql_dump_exe_dir():
    path = filedialog.askopenfilename(initialdir="/", title=translate('choose_mysql_dump_exe_dir'), filetypes=(("exe files", "*.exe"),("all files", "*.*"))) 
    mysql_dump_exe_entry.delete(0, customtkinter.END)
    mysql_dump_exe_entry.insert(0, path)

# Function to Select All Databases
def select_all_databases():
    for db, var in checkbox_vars.items():
        var.set(True)

# Function to Unselect All Databases
def unselect_all_databases():
    for db, var in checkbox_vars.items():
        var.set(False)

# Save the Config and Translation in Varaibles
config = load_config()
translation, languages = load_language(config.get('language'))

# Basic GUI Settings
customtkinter.set_appearance_mode(config['background_theme'].lower())
customtkinter.set_default_color_theme(config['theme_color'].lower())

# Create GUI
app = customtkinter.CTk()

# Add Title and set Size
app.title('Lux_MySQLBackup')
app.geometry("600x460")

# disable resize
app.resizable(False, False)

# Create Tab View
tabView = customtkinter.CTkTabview(app)
tabView.pack(padx=20, pady=20)

# Generall Settings
# Add General Settings Tab to Tab View
general_tab = tabView.add(translate('general_settings_tab'))

# Language Input
language_dropdown_label = customtkinter.CTkLabel(general_tab, text=translate('language'))
language_dropdown_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='w')

language_dropdown_field_str_var = customtkinter.StringVar(value=config.get('language'))
language_dropdown_field = customtkinter.CTkOptionMenu(general_tab, values=languages, variable=language_dropdown_field_str_var)
language_dropdown_field.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='w')

# Date Format Input 
date_format_label = customtkinter.CTkLabel(general_tab, text=translate('date_format'))
date_format_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')

date_format = customtkinter.CTkEntry(general_tab, width=200, height=30, border_width=2, corner_radius=10)
date_format.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='w')

# Backup Directory Input
backup_dir_label = customtkinter.CTkLabel(general_tab, text=translate('backup_path'))
backup_dir_label.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')

backup_dir_entry = customtkinter.CTkEntry(general_tab, width=200, height=30, border_width=2, corner_radius=10)
backup_dir_entry.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='w')

backup_dir_button = customtkinter.CTkButton(general_tab, text='...', width=30, command=select_backup_dir)
backup_dir_button.grid(row=2, column=1, padx=(210, 10), pady=10, sticky='w')

# Backup Count Input 
backup_count_label = customtkinter.CTkLabel(general_tab, text=translate('backup_count'))
backup_count_label.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='w')

backup_count_entry = customtkinter.CTkEntry(general_tab, width=200, height=30, border_width=2, corner_radius=10)
backup_count_entry.grid(row=3, column=1, padx=(5, 10), pady=10, sticky='w')

# MySQL.exe Path Input
mysql_exe_label = customtkinter.CTkLabel(general_tab, text=translate('mysql_exe_path'))
mysql_exe_label.grid(row=4, column=0, padx=(10, 5), pady=10, sticky='w')

mysql_exe_entry = customtkinter.CTkEntry(general_tab, width=200, height=30, border_width=2, corner_radius=10)
mysql_exe_entry.grid(row=4, column=1, padx=(5, 10), pady=10, sticky='w')

mysql_exe_button = customtkinter.CTkButton(general_tab, text='...', width=30, command=select_mysql_exe_dir)
mysql_exe_button.grid(row=4, column=1, padx=(210, 10), pady=10, sticky='w')

# MySQLDump.exe Path Input
mysql_dump_exe_label = customtkinter.CTkLabel(general_tab, text=translate('mysql_dump_exe_path'))
mysql_dump_exe_label.grid(row=5, column=0, padx=(10, 5), pady=10, sticky='w')

mysql_dump_exe_entry = customtkinter.CTkEntry(general_tab, width=200, height=30, border_width=2, corner_radius=10)
mysql_dump_exe_entry.grid(row=5, column=1, padx=(5, 10), pady=10, sticky='w')

mysql_dump_exe_button = customtkinter.CTkButton(general_tab, text='...', width=30, command=select_mysql_dump_exe_dir)
mysql_dump_exe_button.grid(row=5, column=1, padx=(210, 10), pady=10, sticky='w')


# Database Connection
# Add Database Connection Tab to Tab View
databse_connection_tab = tabView.add(translate('database_connection_tab'))

# Hostname Input
hostname_label = customtkinter.CTkLabel(databse_connection_tab, text=translate('hostname'))
hostname_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')

hostname_entry = customtkinter.CTkEntry(databse_connection_tab, width=200, height=30, border_width=2, corner_radius=10)
hostname_entry.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='w')

# Username Input
database_user_label = customtkinter.CTkLabel(databse_connection_tab, text=translate('database_user'))
database_user_label.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')

database_user_entry = customtkinter.CTkEntry(databse_connection_tab, width=200, height=30, border_width=2, corner_radius=10)
database_user_entry.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='w')

# Password Input
database_password_label = customtkinter.CTkLabel(databse_connection_tab, text=translate('database_password'))
database_password_label.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='w')

database_password_entry = customtkinter.CTkEntry(databse_connection_tab, width=200, height=30, border_width=2, corner_radius=10, show='*')
database_password_entry.grid(row=3, column=1, padx=(5, 10), pady=10, sticky='w')

# Databases 
# Add Databases Tab to Tabview
databases_tab = tabView.add(translate('databases_tab'))

# Make Database tab Flexible
databases_tab.grid_columnconfigure(0, weight=1)  # Left
databases_tab.grid_columnconfigure(1, weight=1)  # Right

databases = get_databases()

if databases == []:
    select_databases_label = customtkinter.CTkLabel(databases_tab, text=translate('no_databases'))
    select_databases_label.grid(row=0, column=0, columnspan=2, pady=(10, 10), padx=10, sticky="nsew")
else:
    select_databases_label = customtkinter.CTkLabel(databases_tab, text=translate('choose_databases_to_backup'))
    select_databases_label.grid(row=0, column=0, columnspan=2, pady=(10, 10), padx=10, sticky="nsew")

    select_all_databases_button = customtkinter.CTkButton(databases_tab, text=translate('select_all_databases'), command=select_all_databases)
    select_all_databases_button.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="ew")

    unselect_all_databases_button = customtkinter.CTkButton(databases_tab, text=translate('unselect_all_databases'), command=unselect_all_databases)
    unselect_all_databases_button.grid(row=1, column=1, padx=(5, 10), pady=10, sticky="ew")

    databases_scrollable_frame = customtkinter.CTkScrollableFrame(databases_tab, width=500, height=200)
    databases_scrollable_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 10))

# Create Database Label and Checkboxes
for idx, db in enumerate(databases):
    label = customtkinter.CTkLabel(databases_scrollable_frame, text=db, anchor="w")
    label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

    var = customtkinter.BooleanVar() 
    checkbox = customtkinter.CTkCheckBox(databases_scrollable_frame, text="", variable=var)
    checkbox.grid(row=idx, column=1, padx=150, pady=5)

    checkbox_vars[db] = var

# Encryption
# Add Encryption Tab to Tabview
encryption_tab = tabView.add(translate('encryption_tab'))

# Use Encryption Checkbox
use_encryption_label = customtkinter.CTkLabel(encryption_tab, text=translate('use_encryption'))
use_encryption_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')

use_encryption_checkbox_var = customtkinter.BooleanVar()
use_encryption_checkbox = customtkinter.CTkCheckBox(encryption_tab, text="", variable=use_encryption_checkbox_var)
use_encryption_checkbox.grid(row=1, column=1, padx=10, pady=5)

# Encryption Password Input
encryption_password_label = customtkinter.CTkLabel(encryption_tab, text=translate('encryption_password'))
encryption_password_label.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')

encryption_password_entry = customtkinter.CTkEntry(encryption_tab, width=200, height=30, border_width=2, corner_radius=10, show='*')
encryption_password_entry.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='w')

# Theme
# Add Theme Tab to Tabview
theme_tab = tabView.add(translate('theme_tab'))

# Backgroud Theme Input
background_theme_label = customtkinter.CTkLabel(theme_tab, text=translate('background_theme'))
background_theme_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='w')

background_theme_str_var = customtkinter.StringVar(value=config.get('background_theme'))
background_theme_dropdown = customtkinter.CTkOptionMenu(theme_tab, values=['System', 'Dark', 'Light'], variable=background_theme_str_var)
background_theme_dropdown.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='w')

# Theme Input 
theme_color_label = customtkinter.CTkLabel(theme_tab, text=translate('theme_color'))
theme_color_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')

theme_color_str_var = customtkinter.StringVar(value=config.get('theme_color'))
theme_color_dropdown = customtkinter.CTkOptionMenu(theme_tab, values=['Blue', 'Green', 'Dark-Blue'], variable=theme_color_str_var)
theme_color_dropdown.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='w')

# Add Save Button
save_button = customtkinter.CTkButton(app, text=translate('save'), command=save_settings)
save_button.place(relx=0.5, rely=0.935, anchor=tkinter.CENTER)

# start the fill in and open the GUI
fill_in_values()
app.mainloop()