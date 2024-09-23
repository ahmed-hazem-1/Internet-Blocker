# Project Title: Admin Controller

## Description
This project is a Python-based application that provides functionalities to manage installed applications on a Windows system. It uses PyQt5 for the GUI and interacts with the Windows Registry and Firewall to perform its operations.

## Features
1. **Application Extraction**: The project can extract a list of installed applications on the system by querying the Windows Registry. This is done in the `AppExtractor.py` file.

2. **Application Blocking**: The project can block any installed application from accessing the internet by creating a new outbound rule in the Windows Firewall. This is done using the `block_program` function in the `AppExtractor.py` file.

3. **Firewall Rule Deletion**: The project can also delete any previously created firewall rule, effectively unblocking the application. This is done using the `delete_firewall_rule` function in the `AppExtractor.py` file.

4. **GUI**: The project uses PyQt5 to create a user-friendly interface for managing the applications. The GUI code is located in the `ListItem.py` file.

## Requirements
- Python 3
- PyQt5
- pywin32

## Usage
To run the project, execute the `run.bat` file. This will start the Python script as an administrator.

```batchfile
@echo off
set PYTHON_SCRIPT="D:\PyQt Projects\Admin Controller\main.py"

echo Running script as Administrator...
powershell -Command "Start-Process cmd -ArgumentList '/c py -3 %PYTHON_SCRIPT%' -Verb RunAs"
```

## Note
This project is intended for educational purposes and should be used responsibly. Always ensure you have the necessary permissions before blocking or unblocking applications.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
