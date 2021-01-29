import paramiko
import datetime
import time
import concurrent
import hashlib
import getpass
import sys

todays_date = datetime.datetime.now()
year = todays_date.year
day = todays_date.day
month = todays_date.month

# get device info
device_info = {
    'hostname': '192.168.0.191',
    'password': getpass.getpass(prompt='Enter your user passowrd: '.strip(), stream=sys.stderr),
    'port': '22',
    'username': 'admin',
    'allow_agent': False,
    'look_for_keys': False
}
enter = '\n'

#build ssh_client
ssh_client = paramiko.SSHClient();

#connect to client
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(**device_info)

    #check if connected
is_connected = ssh_client.get_transport().is_active()


# build shell for client
device_shell = ssh_client.invoke_shell()
device_shell.send(f'terminal length 0{enter}')
device_shell.send(f'show users{enter}')

time.sleep(2)

output = device_shell.recv(10000).decode('utf-8')

convert_output = output.split(enter)
# print(convert_output)

def out_to_file(output):
    with open(f"{device_info['hostname']}_output_{month}_{day}_{year}.cfg", 'w') as output_file:
        for line in output:
            output_file.write(line)
    return

out_to_file(convert_output)

if __name__ == '__main__':
    print('Running from main script!')

# send commands to client