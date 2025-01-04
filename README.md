# Lux_MySQLBackup
Simple MySQL Backup with Python for Windows

# Installtion 
1. Download Ping over Port.py
2. Open Python file and edit the Translation in line 16 
3. Edit Date Format in line 19
4. Add Hostname, Username and Password in line 111
5. Define Backup Folder  and how many Backups sould be saved in line 116
6. Define MySQL and MySQL Dump Path in line 120 (In my case i use MariaDB 11.5 there will the path be filled in by default)
7. Define the Databases that sould exlude in line 124
8. Place the File in eg. C:\Backup
9. Open the Windows Taskplaner
10. Create an Simple New task and Define a Name
11. Define how often the Backup sould be run
12. By Action tab you couse Start Programm
13. In Field Progreem use the Path to the Prowershell.exe (by default C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe)
14. In Fíeld Arguments Paste: -command "python '[path to Lux_MySQLBackup.py File]'"
15. Hit save

# License 

MIT License  

Copyright (c) 2024 LuxCoding

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Thx for using my MySQL Backup
