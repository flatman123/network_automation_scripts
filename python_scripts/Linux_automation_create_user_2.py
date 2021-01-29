import paramiko
import time

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

linux_box = {
    'hostname': '192.168.0.130',
    'password': 'cisco123',
    'username': 'jeffmci',
    'port': '22',
    'allow_agent': False,
    'look_for_keys': False
}
# time.sleep(3)
print(f'Connecting to Host {linux_box["hostname"]}...')
ssh_client.connect(**linux_box)

''' Executing commands on a linux box using exec
The exec will return a tuple with three outputs '''

stdin, stdout, stderr = ssh_client.exec_command('ip address show\n')
linux_output = stdout.read()
linux_output = linux_output.decode()
print(linux_output)

stdin, stdout, stderr = ssh_client.exec_command('sudo adduser jamila\n', get_pty=True)
time.sleep(2)
stdin.write('admin123')

stdin, stdout, stderr = ssh_client.exec_command('sudo cat /etc/passwd\n')
time.sleep(3)
new_output = stdout.read().decode()
print()
print(stdout.read())






session_is_active = ssh_client.get_transport().is_active()

ssh_client.close() if session_is_active else print('still active')
