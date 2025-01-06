# Lux_MySQLBackup
Simple MySQL Backup with Python for Windows

# Installation
1. Download all files.
2. Open a terminal.
3. Install customtkinter by using the following command: "pip install customtkinter".
4. Place the files, e.g., in C:\Backup.
5. Start GUI.py, fill in all values, and hit save.
6. The GUI will reopen so you can choose the databases that should be backed up.
7. After selecting the databases, hit save again and close the GUI.
8. Open the Windows Task Scheduler.
9. Create a new simple task and define a name.
10. Define how often the backup should run.
11. In the Action tab, choose "Start Program".
12. In the "Program/script" field, use the path to powershell.exe (by default C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe).
13. In the "Arguments" field, paste: -command "python '[path to Lux_MySQLBackup.py file]'"
14. Hit save.

# FAQ
Q: How can I add another language?
A: Simply open the Language.json and copy, for example, the English part. Then rename it to your desired language and translate the texts.

Q: Where can I find the MySQL.exe and MySQLDump.exe?
A: If you are using MariaDB, the executables should be in the following directory: "C:/Program Files/MariaDB xx.x/bin/". For other MySQL databases, the path may be different.

Q: Why can't I select any databases?
A: You need to set up the values in the General and Database Connection tabs first and hit save. After that, the GUI will reopen, and you can select your databases.



# License 

MIT License  

Copyright (c) 2024 LuxCoding

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Thx for using my MySQL Backup
