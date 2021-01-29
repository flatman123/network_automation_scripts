import os
import hashlib
import getpass
import sys

salt = os.urandom(32)
device_pass = getpass.getpass(prompt='Enter your user passowrd', stream=sys.stderr)

key = hashlib.pbkdf2_hmac('sha256',
                        device_pass.encode('utf-8'),
                        salt,
                        100000,
                        dklen=128)

storage = salt + key

salt_from_storage = storage[:32]
key_from_storage = storage[32:]


# checking if password is correct
print(storage)