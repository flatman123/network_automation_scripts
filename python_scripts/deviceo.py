import time
import paramiko
import requests
import concurrent.futures
import getpass
import sys

#setup the hosts
hosts = ['240', '242', '166']


def send_commands(client_shell, commands, enter='\n'):
    # If using cisco device, uncomment
    client_shell.send(f'terminal length 0{enter}')
    client_shell.send(commands + enter)
    time.sleep(3)
    device_config_output = client_shell.recv(10000).decode('utf-8')

    session_active = client_shell.get_transport().is_active()

    if session_active:
        client_shell.close()
        
    return device_config_output

#setup shell for client
def build_shell(client, host_ip):
    print(f'Building Shell for host {host_ip}')
    time.sleep(3)
    shell = client.invoke_shell()
    print(f'Shell for host {host_ip} built...')
    return shell


#Connect to host
def connect_to_client(client, host_ip, username, pwd, port='22', allow_ag=False, look_ky=False):
    client_info = {
        'hostname': host_ip,
        'port': '22',
        'password': pwd,
        'username': username,
        'allow_agent': allow_ag,
        'look_for_keys': look_ky    
    }
    client.connect(**client_info)
    return client


#setup the ssh_client
def build_ssh_client(host_ip):    
    print(f'Building ssh client for host {host_ip}')
    ssh_client = paramiko.SSHClient()
    time.sleep(3)

    print(f'Adding ssh_client policys for host {host_ip}')   
    time.sleep(3)   
    
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'SSH client built...')
    time.sleep(3)
    
    print(f'Connecting to host {host_ip}...')
   
    return ssh_client





if __name__ == '__main__':
    build_ssh_client('192.168.0.240')
    




