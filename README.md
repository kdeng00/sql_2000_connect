# sql_2000_connect
A short Python program that demonstrates connecting to a SQL Server 2000 database. The demo simply retrieves results from the [JobMessageQueue]
SQL table and prints them out to the console.

## Non-standard libraries used
* pyodbc


### Getting started
Fairly simple in getting this demo working, this demo is intended to work on Windows operating systems. This was tested on Windows 10, although it's expected to work for Windows Operating Systems from Windows 7 to Windows 10. Prior to cloning the repository ensure that the following has been addressed:

1. Install Python (Python3 or greater)
2. Install pip
3. Install virtualenv
4. Install the SQL Native Client driver


May have to add python, pip, and virtualenv to the PATH enviornment in order to call the software from the command line

## Building and running
Clone the repository to a directory of your choice and enter the directory.
```Bash
git clone https://github.com/a1admin/sql_2000_connect
cd sql_2000_connect
```

Ensure the ``connection_string.json`` file contains the appropriate values to connect to the SQL Server 2000 database.

``connection_string.json``
```Json
{
    "driver": "SQL Native Client",
    "server": "servername",
    "database": "databasename",
    "username": "admin",
    "password": "password"
}
```

Create a virtuel environment using ``virtualenv`` and activate the environment

```Bash
virtualenv env
env\Scripts\activate
```

A new virtual enviornment was created in the env directory. The purpose of this is to contain packages/dependencies of the software to be within
the project and not installed on the system. This makes it easy when working on the same project with multiple people. For the most part no need
to worry about project dependencies that haven't been installed.

Install the ``pyodbc`` dependency required for this project
```Bash
pip3 install -r requirements.txt
```

Now run the program and pass the path of the ``connection_string.json`` as a command line argument.
```Bash
python3 main.py path\to\connection_string.json
```

The result is the last 15 [JobMessageQueue] records created at the time the program fetched the results. In other words, if one were to run this
program again, the results might change due to a message being queued to a user.