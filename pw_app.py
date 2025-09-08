import os
from password_manager import PasswordManager
from string import punctuation, ascii_lowercase, ascii_uppercase, digits
import random as r

def initial_setup(file_name):
    """
    create the passwords file and add the master username and password as the first entry
    returns: instance of the PasswordManager class with information from the current session
    """
    username = input('Username: ').strip()
    password = input('Password: ')
    
    if not file_name:
        user = PasswordManager(username, password)
    else:
        user = PasswordManager(username, password, file_name)
        
    while True:
        try:
            user.validate_entries(user.username, user.password, invalid_characters)
        except ValueError as e:
            print(e)
            user.username = input('Username: ').strip()
            user.password = input('Password: ')
        else:
            user.create_account()
            print('-' * 20)
            print('User created successfully!')
            print('-' * 20)
            
            return user

def subsequent_uses(file_name):
    """
    log the user in
    max attempts: 3
    if max attempts are exceeded, the app will exit
    returns: user upon successful login and False otherwise
    """
    username = ''
    password = ''
    
    if not file_name:
        user = PasswordManager(username, password)
    else:
        user = PasswordManager(username, password, file_name)
    for _ in range(3):
        user.username = input('Username: ').strip()
        user.password = input('Password: ')
        if user.login():
            user.load_passwords()
            return user
        else:
            print('-' * 20)
            print('Invalid username or password')
            print('-' * 20)

    return False

def add_password(user):
    """
    updates the passwords attribute of the user instance with new entry
    uses a system generated password if the user desires
    """
    while True:
        service_name = input('Please enter the name of the service: ').strip()
        if not service_name:
            print('Service name must not be empty')
        else:
            break
    
    if service_name in user.passwords:
        return False
    
    username = input('Username: ')
    while True:
        generate = input('Would you like to generate a password [y/n]? ').lower().strip()
     
        if not generate:
            generate = 'y'
        if generate not in ['yes', 'y', 'no', 'n']:
            print('Invalid choice. Please try again.')
        else:
            break
        
    if generate in ['yes', 'y']:
        while True:
            length = input('Length (Default 8): ')
            
            if not length:
                length = 8
                break

            try:
                length = int(length)
                if 1 <= length <= 20:
                    break
                else:
                    print('Please enter a number between 1 and 20.')
            except ValueError:
                print('Please enter a valid number.')
                
        while True:
            nums = input('Include numbers [y/n]? ').lower().strip()
            
            if not nums:
                nums = 'y'
            if nums in ['yes', 'y', 'no', 'n']:
                break
            else:
                print('Invalid choice.')
            
        while True:
            symbols = input('Include symbols [y/n]? ').lower().strip()
            
            if not symbols:
                symbols = 'y'
            if symbols in ['yes', 'y', 'no', 'n']:
                break
            else:
                print('Invalid choice. Please try again.')
        
        password = generate_password(length, nums, symbols)
    else:
        password = input('Password: ')
    
    while True:
        try:
            PasswordManager.validate_entries(username, password, invalid_characters)
        except ValueError as e:
            print('-' * 20)
            print(e)
            print('-' * 20)
            username = input('Username: ').strip()
            if generate not in ['yes', 'y']:
                password = input('Password: ')
        else:
            user.update_passwords({service_name.lower(): {'username': username, 'password': password}})
            return True
        
def generate_password(length, nums, symbols):
    """
    Generates and returns a random password based on the user's specification
    """
    password = []
    possible_chars = []
    #create a list that guarantees one of each type of character, ONLY IF the length allows (e.g., password of length 1 cannot contain a digit and a symbol)
    guaranteed_chars = []
    
    guaranteed_chars.append(r.choice(ascii_lowercase))
    guaranteed_chars.append(r.choice(ascii_uppercase))
    possible_chars += list(ascii_lowercase + ascii_uppercase)
    
    if nums in ['yes', 'y']:
        possible_chars += list(digits)
        guaranteed_chars.append(r.choice(digits))
    if symbols in ['yes', 'y']:
        #create a translate table that removes the invalid characters from the possible choices
        allowed_punctuation = punctuation.translate(str.maketrans('', '', ''.join(invalid_characters)))
        possible_chars += list(allowed_punctuation)
        guaranteed_chars.append(r.choice(allowed_punctuation))
    
    #Check if the given length is enough to include one of each type of character
    if length >= len(guaranteed_chars):
        password += guaranteed_chars
        
        for _ in range(length - len(guaranteed_chars)):
            password.append(r.choice(possible_chars))
    else:
        for _ in range(length):
            password.append(r.choice(possible_chars))
    
    r.shuffle(password)
    
    return ''.join(password)

def delete(user):
    fieldname = input('Please enter the name of the service you would like to delete: ').lower()
    
    if fieldname not in user.passwords:
        return False

    user.delete_entry(fieldname)
    
    return True

def password_manager():
    file_name = input('Welcome to password manager! Please enter the name of your file: (press enter to use "passwords.csv") ').strip()
    if file_name and not file_name.endswith('.csv'):
        file_name += '.csv'
    if not os.path.exists(file_name if file_name else PasswordManager.default_filename):
        user = initial_setup(file_name)
    else:
        user = subsequent_uses(file_name)
        if not user:
            print('-' * 20)
            print('Max attempts exceeded. Exiting application.')
            print('-' * 20)
            
            return

    while True:
        choice = input('Please select from one of the following choices:\n1. View passwords\n2. Add password\n3. Delete password\n4. Exit\n').strip()
        if not choice:
            choice = '1'
        if choice not in ['1', '2', '3', '4']:
            print('-' * 20)
            print('Invalid choice')
            print('-' * 20)
        elif choice == '4':
            user.update_file()
            break
        elif choice == '1':
            print('-' * 80)
            for servicename, credentials in user.passwords.items():
                print('Service:', servicename, '| Username:', credentials['username'], '| Password:', credentials['password'])
            print('-' * 80)
        elif choice == '2':
            if not add_password(user):
                print('-' * 20)
                print('Service already exists.')
                print('-' * 20)
            else:
                print('-' * 20)
                print('Service successfully added!')
                print('-' * 20)
        else:
            if not delete(user):
                print('-' * 20)
                print('Record not found.')
                print('-' * 20)
            else:
                print('-' * 20)
                print('Service successfully deleted!')
                print('-' * 20)

if __name__ == '__main__':
    invalid_characters = [',', '=', ' ']
    password_manager()