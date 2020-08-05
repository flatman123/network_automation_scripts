import paramiko
import time
import datetime
import getpass
import sys

get_user = input('Admin please enter your username: ')
get_pass = getpass.getpass(prompt='Enter your password: ', stream=sys.stderr)
enter = '\n'

linux_box = {
    'hostname': '192.168.0.176',
    'username': get_user,
    'port': '22',
    'password': get_pass,
    'look_for_keys': False,
    'allow_agent': False

}
# so the script must connecte to the linux terminal

#build ssh client
ssh_client = paramiko.SSHClient()

#disregard the keys
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#connect to host
connect = ssh_client.connect(**linux_box)
session_is_active = ssh_client.get_transport().is_active()

shell = ssh_client.invoke_shell()
# shell.send(f'pwd {enter}')

#Get username to add
new_user = input('What is the name of the new user? ').strip()
shell.send(f'sudo useradd {new_user} {enter}')

#admin password
shell.send(f'{get_pass}{enter}')

#get password to add
add_password = getpass.getpass(prompt='What password to add for the user? ', stream=sys.stderr)
shell.send(f'{add_password} {enter}')
shell.send(f'{add_password} {enter}')

shell.send(f'cat /etc/passwd | tail {enter}')
time.sleep(2)
output = shell.recv(10000).decode('utf-8')
print(output)


