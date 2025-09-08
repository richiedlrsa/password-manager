# PyManager
Your all-in-one command-line password manager.

## Description

This password manager allows users to store and manage login credentials for various services. It includes a master login, and all data is saved locally to a .csv file. You can view, add, and delete passwords using the CLI.

## Key Features
* **Master Login**: Protects all your passwords with a single master username and password.
* **Functionality**: Easily add, view and delete password entries.
* **Local Storage**: All passwords are saved in a CSV file in the same directory for more control.
* **Password Generator**: Automatically generate a strong random password based on your criteria (length, inclusion of numbers and symbols).
* **Input Validation**: Implements checks on username/password for length and character restrictions.

## Prerequisites

Make sure both password_manager.py and pw_app.py are in the same folder.

## How to use

1. **Launch**: When you run the app, you'll be asked for a filename for your password storage file. You can enter a name or simply press <ENTER> to use the default (passwords.csv).
2. **First-Time Setup**: If it's your first time using that filename, you'll be prompted to create your master username and password.
3. **Login**: On subsequent uses, you'll need to log in with your master credentials. You have three attempts before the app exits.
4. **Main Menu**: Once logged in, you can choose from the following options:
    1. **View passwords**: Shows all your saved credentials.
    2. **Add password**: Prompts you to add a new service. New entries are saved to the storage file only when you exit the app.
    3. **Delete password**: Allows you to remove an existing entry using the service name.
    4. **Exit**: Saves all changes (additions/deletions) to the password storage file and closes the app.


## Important
* **Usernames** must be at least **4** characters long.
* **Passwords** must be at least **1** character long.
* Passwords **cannot** contain commas (,), equal signs (=), or spaces.
* Service names cannot be empty
* Service names are case insensitive. 'Gmail' will be treated the same as 'gmail'.
