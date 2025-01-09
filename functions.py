import ctypes
from ctypes import wintypes
import base64
import json
import os
import subprocess

def get_script_dir():
    script_dir = os.path.dirname(__file__)
    return script_dir

# Struckture for DATA_BLOB
class DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ("cbData", wintypes.DWORD),
        ("pbData", ctypes.POINTER(ctypes.c_byte)),
    ]

# Funcstion helps to create DATA_BLOP ot of Bytes
def _blob(data):
    blob = DATA_BLOB()
    blob.cbData = len(data)
    blob.pbData = ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_byte))
    return blob

# Function to Encryt Data with DAPAPI and returns Base64-coded Data
def encrypt(data):
    data_blob_in = _blob(data.encode('utf-8'))
    data_blob_out = DATA_BLOB()

    if ctypes.windll.crypt32.CryptProtectData(
        ctypes.byref(data_blob_in),  # Data to encrypt
        None,                        # Description (optional)
        None,                        # Entropy key (optional)
        None,                        # Reserved
        None,                        # Prompt struct (optional)
        0,                           # Flags
        ctypes.byref(data_blob_out)  
    ):
        # Convert data in Base64 and return them
        encrypted_data = ctypes.string_at(data_blob_out.pbData, data_blob_out.cbData)
        ctypes.windll.kernel32.LocalFree(data_blob_out.pbData) 
        return base64.b64encode(encrypted_data).decode('utf-8')
    else:
        raise ctypes.WinError()

# Funcstion to Decrypt Base64-coded Data with DAPAPI
def decrypt(encrypted_data):
    try:
        data_blob_in = _blob(base64.b64decode(encrypted_data))
        data_blob_out = DATA_BLOB()

        if ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(data_blob_in),  # Encryped Data
            None,                        # Description (optional)
            None,                        # Entropy key (optional)
            None,                        # Reserved
            None,                        # Prompt struct (optional)
            0,                           # Flags
            ctypes.byref(data_blob_out)  
        ):
            # reutrn Decrypted data
            decrypted_data = ctypes.string_at(data_blob_out.pbData, data_blob_out.cbData)
            ctypes.windll.kernel32.LocalFree(data_blob_out.pbData)
            return decrypted_data.decode('utf-8')
        else:
            raise ctypes.WinError()
    except:
        return ""
    
# Function to load the Config File
def load_config():
    try:
        with open(os.path.join(get_script_dir(), 'settings.json'), 'r', encoding='utf-8') as f:
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
        with open(os.path.join(get_script_dir(), 'language.json'), 'r', encoding='utf-8') as f:
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
config = load_config()
translation, languages = load_language(config.get('language'))

def translate(key, **kwargs):
    text = translation.get(key, key)  
    try:
        return text.format(**kwargs) 
    except KeyError:
        return text

# function to save the Confing to the Config file
def save_config(config):
    try:
        with open(os.path.join(get_script_dir(), 'settings.json'), "w", encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(translate('error_by_saving_config', e=e))
        return None
    
# Funcstion to get all Databases
def get_databases():
    try:
        cmd = [
            config.get('mysql_exe_path'),
            '-h', decrypt(config.get('hostname')),
            '-u', decrypt(config.get('database_password')),
            f'--password={decrypt(config.get('database_password'))}',
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