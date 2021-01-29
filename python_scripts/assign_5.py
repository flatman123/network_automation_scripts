import paramiko
import time

# creating an ssh client object
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print('Connecting to 192.168.0.191')
ssh_client.connect(hostname='192.168.0.191', port='22', username='admin', password='cisco123',
                   look_for_keys=False, allow_agent=False)


shell = ssh_client.invoke_shell()
shell.send('terminal length 0\n')
shell.send('show ip int brief\n')
time.sleep(1)
# Error solution...was not decoding the strings
output = shell.recv(100000).decode('utf-8')
print(output)


if ssh_client.get_transport().is_active():
    print('Closing connection')
    ssh_client.close()