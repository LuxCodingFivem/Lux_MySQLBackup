"""
Lux_MySQLBackup

Copyright (c) 2025 LuxCoding

This script is licensed under the MIT License.
For full details, see the LICENSE file in the repository.
"""
# Import requiered Libs
from tkinter import filedialog
import tkinter
import customtkinter
import os
import subprocess
import sys
from py.functions import load_config
from py.functions import load_language
from py.functions import translate
from py.functions import decrypt_file

# Save the Config and Translation in Varaibles
config = load_config()
translation, languages = load_language(config.get('language'))

script_dir = os.path.dirname(__file__)

# Function to Restart GUI
def restart_GUI():
    app.destroy()
    subprocess.Popen([sys.executable, os.path.join(script_dir, 'Decrypt backup GUI.py')])

# Select the Input File
def select_input_file():
    path = filedialog.askopenfilename(initialdir="/", title=translate('choose_input_file'), filetypes=(("sql files", "*.sql"),("all files", "*.*"))) 
    input_file_entry.delete(0, customtkinter.END)
    input_file_entry.insert(0, path)

# Function to Select output Path
def select_output_path():
    path = filedialog.askdirectory(initialdir="/", title=translate('choose_output_path'))
    output_file_path_entry.delete(0, customtkinter.END)
    output_file_path_entry.insert(0, path)

def decrypt_button_action():
    try:
        file_name = output_file_name_entry.get()
        if not file_name.endswith('.sql'):
            file_name += '.sql'

        output_file_path = os.path.join(output_file_path_entry.get(), file_name)
        decrypt_file(input_file_entry.get(), output_file_path, decrypt_password_entry.get())
        restart_GUI()
    except ValueError as e:
        print(e)

# Basic GUI Settings
customtkinter.set_appearance_mode(config['background_theme'].lower())
customtkinter.set_default_color_theme(config['theme_color'].lower())

# Create GUI
app = customtkinter.CTk()

# Add Title and set Size
app.title(translate('decrypt_gui_title'))
app.geometry("500x280")

# disable resize
app.resizable(False, False)

# Frame Where all Items will be in
frame = customtkinter.CTkFrame(app)
frame.pack(padx=20, pady=20)

# Decryption Password Input
decrypt_password_label = customtkinter.CTkLabel(frame, text=translate('decrypt_password'))
decrypt_password_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='w')

decrypt_password_entry = customtkinter.CTkEntry(frame, width=200, height=30, border_width=2, corner_radius=10, show="*")
decrypt_password_entry.grid(row=1, column=1, padx=(5, 10), pady=10, sticky='w')

# File Input 
input_file_label = customtkinter.CTkLabel(frame, text=translate('input_file'))
input_file_label.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='w')

input_file_entry = customtkinter.CTkEntry(frame, width=200, height=30, border_width=2, corner_radius=10)
input_file_entry.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='w')

input_file_button = customtkinter.CTkButton(frame, text='...', width=30, command=select_input_file)
input_file_button.grid(row=2, column=1, padx=(210, 10), pady=10, sticky='w')

# Output File name Input
output_file_name_label = customtkinter.CTkLabel(frame, text=translate('Output_file_name'))
output_file_name_label.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='w')

output_file_name_entry = customtkinter.CTkEntry(frame, width=200, height=30, border_width=2, corner_radius=10)
output_file_name_entry.grid(row=3, column=1, padx=(5, 10), pady=10, sticky='w')

# Output File Path Input
output_file_path_label = customtkinter.CTkLabel(frame, text=translate('output_file_path'))
output_file_path_label.grid(row=4, column=0, padx=(10, 5), pady=10, sticky='w')

output_file_path_entry = customtkinter.CTkEntry(frame, width=200, height=30, border_width=2, corner_radius=10)
output_file_path_entry.grid(row=4, column=1, padx=(5, 10), pady=10, sticky='w')

output_file_path_button = customtkinter.CTkButton(frame, text='...', width=30, command=select_output_path)
output_file_path_button.grid(row=4, column=1, padx=(210, 10), pady=10, sticky='w')

# Add Save Button
decrypt_button = customtkinter.CTkButton(master=app, text=translate('decrypt'), command=decrypt_button_action)
decrypt_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

app.mainloop()
