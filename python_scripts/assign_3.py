import paramiko
import datetime
import getpass
import time
import sys

todays_date = datetime.datetime.now()
year = todays_date.year
day = todays_date.day
month = todays_date.month
enter = '\n'

# usr = getpass.getuser()
pwd = getpass.getpass(prompt='Enter password: '.strip(), stream=sys.stderr)

device_info = {
    'hostname': '192.168.0.191',
    'password': pwd,
    'port': '22',
    'username': 'admin',
    'allow_agent': False,
    'look_for_keys': False
}

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(**device_info)

shell = ssh_client.invoke_shell()
shell.send(f'terminal length 0{enter}')
shell.send(f'show run{enter}')

print(f"Generating config for host {device_info['hostname']}")
time.sleep(2)

result = shell.recv(10000).decode('utf-8')
converted_result = result.split(enter)

with open(f"{device_info['hostname']}-{month}-{day}-{year}-backup.txt", 'w') as device_output:
    for line in converted_result:
        device_output.write(line)


if ssh_client.get_transport().is_active():
    ssh_client.close()
