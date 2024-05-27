# generate random number

# function defination,takes no arguement
def gen_random():
    import random

# random is used to generate random numbers and make random selections
    import string

    # provides a collection of strings constants,including digits,letters

# initialize the size of string 
    
    N = 6
    # N is set to six ,specifies the length of the string to be six
    # generate a random 
    res = ''.join(random.choices(string.digits, k=N))
  # ''.join() it concantenates the random strings to single strings 
    # print the result
    print("The generated string is : "+str(res))
    return str(res)
# gen_random()



# Check phone validity 

import re

# its a module that provides support for working with regular expressions

def check_phone(phone):

    # the function takes one arguement 
    regex = "^\+254\d{9}"
    

    # ^ it asserts the start of the string
    # \+254 it matches the literal string +254
    # \d {9} matches exactly nine digits
    if not re.match(regex,phone) or len (phone) !=13:
        print("Invalid phone number")
        return False
    else:
        print("Valid phone number")
        return True
# check_phone("+254769963584") 
    
    # check password validity
import re
def password_validity(password):

    if len (password) < 8:
        return("password is very short")
    elif not re.search( "[A-Z]", password):
        return("password must contain at least one uppercase letter")
    elif not re.search( "[a-z]", password):
        return("password must contain at least lowercase letters")
    elif not re.search( "[0-9]", password):
        return( "password must contain at least one number")
    elif not re.search( "[!@#$%^&*()_+]", password):
        return("password must contain at least one special character")

    else:
        return True

# password_validity( input("Enter your password: "))
    
    # sending an sms

import africastalking
        
africastalking.initialize(
username="joe2022",
api_key="aab3047eb9ccfb3973f928d4ebdead9e60beb936b4d2838f7725c9cc165f0c8a"
#justpaste.it/1nua8
)
sms = africastalking.SMS

def send_sms(phone,  message):
    recipients = [phone]
    sender = "AFRICASTALKING"
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as error:
        print("Error is :", error)

# send_sms("+254769963584","This is my message")

# hash password
import bcrypt
# bcrypt is a module for hashing and checking passwords
# It very secure
def hash_password(password):

    bytes = password.encode( "utf-8")
    # password is encoded into bytes 
    # it is necessary bacause bcrypt library works when we bind data
    # print(bytes)
    salt = bcrypt.gensalt()
    # using a unique salt for each password ensures  that even if two passwords are the same, they will have different hashes
    # print(salt)
    hash = bcrypt.hashpw( bytes, salt) 
    # print(hash)
    return hash.decode("utf-8")

# hash_password(input( "Enter your password: "))

# Verify password 

def verify_password(password,hash_password):
    bytes = password.encode("utf-8")
    result = bcrypt.checkpw(bytes,hash_password.encode( "utf-8"))
    print(result)
    return result

# verify_password("12345","$2b$12$/DVoD13Ana0j3tjp0zNw2OehATz0qMpNh7DFHJjXSxwl3w9HYl2ze")
    
# encrypt data
from cryptography.fernet import Fernet
# We import fernet class
# The module is used for encryption and decryption.

def generate_key():
    # Its a function used to generate a new encryption key
    key = Fernet.generate_key()
    # print(key)
    with open ("key.key","wb") as key_file: 
        # with open opens a new file if it exists 
        # creates a new file if does not exist
        # wb-write binary -ensures the file is properly closed after writing on it
        key_file.write(key)

# generate_key()
        
# Load key
def  load_key():
    return open("key.key", "rb").read()
# it reads the entire content of the file 

# load_key()

# encrypt data
def encrypt_data(data):
    key = load_key()
    f= Fernet(key)
    # print(f)
    # This creates a fernet object for encryption

    encrypted_data = f.encrypt( data.encode())
    print(encrypted_data.decode())
    # return encrypt_data
    

# encrypt_data("1234")
    
# Decrypt data
    
def decrypt_data(encrypted_data):
    key  = load_key()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data.encode())
    print(decrypted_data.decode())
decrypt_data("gAAAAABmUENSPDlRrA7er0WbYBe-qmblg0zVlOfF278UCpK8UP_VOgHNGRLk-FwqhpcGCCvYZv-y82ylnGYATr25QkXUgDjQbg==")



    


        
