"""
Lux_MySQLBackup GUI

Copyright (c) 2024 LuxCoding

This script is licensed under the MIT License.
For full details, see the LICENSE file in the repository.
"""
# Import requiered Libs
import json
import customtkinter 
import tkinter
from tkinter import filedialog
import os
import subprocess

checkbox_vars = {}

# Gets the curent Script Path and store it in a Variable
script_dir = os.path.dirname(__file__)

# Function to Restart GUI
def restart_GUI():
    app.destroy()  
    os.startfile(os.path.join(script_dir, 'GUI.py'))

# Function to load the Config File
def load_config():
    try:
        with open(os.path.join(script_dir, 'settings.json'), 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print('File not fount')
        return None
    except json.JSONDecodeError as e:
        print(f'Error by reading JSON-File: {e}')
        return None

# fucntion to load the Language 
def load_language(language):
    try:
        with open(os.path.join(script_dir, 'language.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)  # JSON laden
            languages = list(data.keys()) 
            
            language_data = data.get(language)
            
            if language_data is None:
                print(f"the Language: '{language}' is not awaiable.")
                return None, languages  
            
            return language_data, languages  
    except FileNotFoundError:
        print("File 'language.json' not found")
        return None, []
    except json.JSONDecodeError as e:
        print(f'Error by Reading JSON-File: {e}')
        return None, []

# function to translate 
def translate(key, **kwargs):
    text = translation.get(key, key)  
    try:
        return text.format(**kwargs) 
    except KeyError:
        return text

# function to save the Confing to the Config file
def save_config(config):
    try:
        with open(os.path.join(script_dir, 'settings.json'), "w", encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(translate('error_by_saving_config', e=e))
        return None

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
    config['database_user'] = database_user_entry.get()
    config['database_password'] = database_password_entry.get()
    config['hostname'] = hostname_entry.get()

    # Databases
    config['databases'] = {}
    for db, var in checkbox_vars.items():
        config['databases'][db] = var.get()

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
    hostname_entry.insert(0, config.get('hostname'))

    database_user_entry.delete(0, customtkinter.END)
    database_user_entry.insert(0, config.get('database_user'))

    database_password_entry.delete(0, customtkinter.END)
    database_password_entry.insert(0, config.get('database_password'))

    # Databases
    for db, value in config['databases'].items():
        if db in checkbox_vars: 
            checkbox_vars[db].set(value) 

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

# Funcstion to get all Databases
def get_databases():
    try:
        cmd = [
            config.get('mysql_exe_path'),
            '-h', config.get('hostname'),
            '-u', config.get('database_password'),
            f'--password={config.get('database_password')}',
            '-e', 'SHOW DATABASES;'
        ]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(translate('error_reqest_database', utf8=result.stderr.decode('utf-8')))
            return []
        
        databases = result.stdout.decode('utf-8').splitlines()[1:]  
        return databases
    except:
        return []

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
app.geometry("500x500")

# Create Tab View
tabView = customtkinter.CTkTabview(app)
tabView.pack(padx=20, pady=20)

# Generall Settings
# Add General Settings Tab to Tab View
tabView.add(translate('general_settings'))

# Language Input
language_dropdown_label = customtkinter.CTkLabel(master=tabView.tab(translate('general_settings')), text=translate('language'))
language_dropdown_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='w')

language_dropdown_field_str_var = customtkinter.StringVar(value=config.get('language'))
language_dropdown_field = customtkinter.CTkOptionMenu(master=tabView.tab(translate('general_settings')), values=languages, variable=language_dropdown_field_str_var)
language_dropdown_field.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='w')

# Date Format Input 
date_format_label = customtkinter.CTkLabel(master=tabView.tab(translate('general_settings')), text=translate('date_format'))
date_format_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')

date_format = customtkinter.CTkEntry(master=tabView.tab(translate('general_settings')), width=200, height=30, border_width=2, corner_radius=10)
date_format.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='w')

# Backup Directory Input
backup_dir_label = customtkinter.CTkLabel(master=tabView.tab(translate('general_settings')), text=translate('backup_path'))
backup_dir_label.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')

backup_dir_entry = customtkinter.CTkEntry(master=tabView.tab(translate('general_settings')), width=200, height=30, border_width=2, corner_radius=10)
backup_dir_entry.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='w')

backup_dir_button = customtkinter.CTkButton(master=tabView.tab(translate('general_settings')), text='...', width=30, command=select_backup_dir)
backup_dir_button.grid(row=2, column=1, padx=(210, 10), pady=10, sticky='w')

# Backup Count Input 
backup_count_label = customtkinter.CTkLabel(master=tabView.tab(translate('general_settings')), text=translate('backup_count'))
backup_count_label.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='w')

backup_count_entry = customtkinter.CTkEntry(master=tabView.tab(translate('general_settings')), width=200, height=30, border_width=2, corner_radius=10)
backup_count_entry.grid(row=3, column=1, padx=(5, 10), pady=10, sticky='w')

# MySQL.exe Path Input
mysql_exe_label = customtkinter.CTkLabel(master=tabView.tab(translate('general_settings')), text=translate('mysql_exe_path'))
mysql_exe_label.grid(row=4, column=0, padx=(10, 5), pady=10, sticky='w')

mysql_exe_entry = customtkinter.CTkEntry(master=tabView.tab(translate('general_settings')), width=200, height=30, border_width=2, corner_radius=10)
mysql_exe_entry.grid(row=4, column=1, padx=(5, 10), pady=10, sticky='w')

mysql_exe_button = customtkinter.CTkButton(master=tabView.tab(translate('general_settings')), text='...', width=30, command=select_mysql_exe_dir)
mysql_exe_button.grid(row=4, column=1, padx=(210, 10), pady=10, sticky='w')

# MySQLDump.exe Path Input
mysql_dump_exe_label = customtkinter.CTkLabel(master=tabView.tab(translate('general_settings')), text=translate('mysql_dump_exe_path'))
mysql_dump_exe_label.grid(row=5, column=0, padx=(10, 5), pady=10, sticky='w')

mysql_dump_exe_entry = customtkinter.CTkEntry(master=tabView.tab(translate('general_settings')), width=200, height=30, border_width=2, corner_radius=10)
mysql_dump_exe_entry.grid(row=5, column=1, padx=(5, 10), pady=10, sticky='w')

mysql_dump_exe_button = customtkinter.CTkButton(master=tabView.tab(translate('general_settings')), text='...', width=30, command=select_mysql_dump_exe_dir)
mysql_dump_exe_button.grid(row=5, column=1, padx=(210, 10), pady=10, sticky='w')


# Database Connection
# Add Database Connection Tab to Tab View
tabView.add(translate('database_connection'))

# Hostname Input
hostname_label = customtkinter.CTkLabel(master=tabView.tab(translate('database_connection')), text=translate('hostname'))
hostname_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')

hostname_entry = customtkinter.CTkEntry(master=tabView.tab(translate('database_connection')), width=200, height=30, border_width=2, corner_radius=10)
hostname_entry.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='w')

# Username Input
database_user_label = customtkinter.CTkLabel(master=tabView.tab(translate('database_connection')), text=translate('database_user'))
database_user_label.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')

database_user_entry = customtkinter.CTkEntry(master=tabView.tab(translate('database_connection')), width=200, height=30, border_width=2, corner_radius=10)
database_user_entry.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='w')

# Password Input
database_password_label = customtkinter.CTkLabel(master=tabView.tab(translate('database_connection')), text=translate('database_password'))
database_password_label.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='w')

database_password_entry = customtkinter.CTkEntry(master=tabView.tab(translate('database_connection')), width=200, height=30, border_width=2, corner_radius=10, show='*')
database_password_entry.grid(row=3, column=1, padx=(5, 10), pady=10, sticky='w')

# Databases 
# Add Databases Tab to Tabview
tabView.add(translate('databases'))

databases = get_databases()

if databases == []:
    select_databases_label = customtkinter.CTkLabel(master=tabView.tab(translate('databases')), text=translate('no_databases'))
else:
    select_databases_label = customtkinter.CTkLabel(master=tabView.tab(translate('databases')), text=translate('choose_databases_to_backup'))
select_databases_label.grid(row=0, column=0, columnspan=2, pady=(10, 10), padx=10, sticky="nsew")

for idx, db in enumerate(databases):
    label = customtkinter.CTkLabel(tabView.tab(translate('databases')), text=db, anchor="w")
    label.grid(row=idx + 1, column=0, padx=10, pady=5, sticky="w")

    var = customtkinter.BooleanVar()  # Variable für die Checkbox
    checkbox = customtkinter.CTkCheckBox(tabView.tab(translate('databases')), text="", variable=var)
    checkbox.grid(row=idx + 1, column=1, padx=10, pady=5)

    checkbox_vars[db] = var

# Theme
# Add Theme Tab to Tabview
tabView.add(translate('theme'))

# Backgroud Theme Input
background_theme_label = customtkinter.CTkLabel(master=tabView.tab(translate('theme')), text=translate('background_theme'))
background_theme_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='w')

background_theme_str_var = customtkinter.StringVar(value=config.get('background_theme'))
background_theme_dropdown = customtkinter.CTkOptionMenu(master=tabView.tab(translate('theme')), values=['System', 'Dark', 'Light'], variable=background_theme_str_var)
background_theme_dropdown.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='w')

# Theme Input 
theme_color_label = customtkinter.CTkLabel(master=tabView.tab(translate('theme')), text=translate('theme_color'))
theme_color_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')

theme_color_str_var = customtkinter.StringVar(value=config.get('theme_color'))
theme_color_dropdown = customtkinter.CTkOptionMenu(master=tabView.tab(translate('theme')), values=['Blue', 'Green', 'Dark-Blue'], variable=theme_color_str_var)
theme_color_dropdown.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='w')

# Add Save Button
save_button = customtkinter.CTkButton(master=app, text=translate('save'), command=save_settings)
save_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

# start the fill in and open the GUI
fill_in_values()
app.mainloop()


# Todo:
#     - Rewrite README
