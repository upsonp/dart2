# Requirements
* Python 3.10+
* Git

# Installation
1. Before installation you must have Python 3.10 and [Git](https://git-scm.com/) installed.

## Windows
1. Open a windows file explorer and navigate to the directory you wish to install DART
1. In the address bar, where the current working directory is specified, type `cmd`
1. In the command window type `git clone http://github.com/upsonp/dart2`
1. When the application has been checked out, close the command window and open the new dart/ directory
1. double click the start_dart.bat file. 

The first time running the application may take several minutes to start while python packages and the inital local database is created. When you see `Listening on TCP address 127.0.0.1:8000` in the command window, open a web browser and enter localhost:8000 in the address bar.

To stop the server, close the command window.

# Settings
Modify the .env file to set your own secret key as well as to point dart to the oracle database where BioChem staging tables will be located. If not creating BioChem staging tables this is unnecessary.

# Starting DART

Once the application has been checked out for the first time, simply naviate to the DART directory and double click the start_dart.bat file. If an internet connection is present the start_dart.bat file will download any required updates from Github. If no internet connection is present the application will appear to hang for a few moments when attempting to connect to github and then will continue without updating.
