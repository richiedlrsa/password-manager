import csv


class PasswordManager:
    fieldnames = ['ServiceName', 'username', 'password']
    default_filename = 'passwords.csv'
    def __init__(self, username, password, file_name=default_filename):
        self.username = username
        self.password = password
        self.file_name = file_name
        self.passwords = {}
    
    def login(self):
        """
        Loads the master username and password from the csv file and validates that the correct username and password was entered
        returns: bool indicating if validation was successful
        """
        with open(self.file_name, 'r') as file:
            csvr = csv.DictReader(file)
            masterpass = next(csvr)
            if self.username != masterpass.get('username', None):
                return False
            if self.password != masterpass.get('password', None):
                return False
            return True
        
    def create_account(self):
        """
        creates a new csv file for password storage and adds the master username and passwords as the first row
        returns: None
        """
        with open(self.file_name, 'w') as file:
            csvw = csv.DictWriter(file, PasswordManager.fieldnames)
            csvw.writeheader()
            csvw.writerow({'ServiceName': 'MasterPassword', 'username': self.username, 'password': self.password})
            
    def load_passwords(self):
        """
        loads the passwords from the passwords file into the passwords attribute as a dictionary of dictionaries
        """
        with open(self.file_name, 'r') as file:
            csvr = csv.reader(file)
            header = next(csvr)
            masterpassword = next(csvr)
            
            for row in csvr:
                self.passwords.update({row[0]: {'username': row[1], 'password': row[2]}})
    
    def update_passwords(self, passwords):
        self.passwords.update(passwords)
        
    def delete_entry(self, servicename):
        self.passwords.pop(servicename)
    
    def update_file(self):
        with open(self.file_name, 'w') as file:
            csvw = csv.DictWriter(file, PasswordManager.fieldnames)
            csvw.writeheader()
            csvw.writerow({'ServiceName': 'MasterPassword', 'username': self.username, 'password': self.password})
            for servicename, credentials in self.passwords.items():
                csvw.writerow({'ServiceName': servicename, 'username': credentials['username'], 'password': credentials['password']})
    
    
    @staticmethod
    def validate_entries(username, password, invalid_characters):
        if len(username) < 4:
            raise ValueError('Username must contain at least 4 characters')
        if len(password) < 1:
            raise ValueError('Invalid password length')
        if any(char in password for char in invalid_characters):
            raise ValueError(f'Password cannot contain commas (,), equal signs (=), or spaces.')