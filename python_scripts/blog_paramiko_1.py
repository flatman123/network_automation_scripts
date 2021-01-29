import paramiko
import time
import getpass
import sys


# OUR GLOBAL VARIABLES
pwd = getpass.getpass(prompt="Enter your password: ".strip(), stream=sys.stderr)
host1 = input("Enter ip for host1: ").strip()
host2 = input("Enter ip for host2: ").strip()
host1_loop = input("Enter loopback address for host1 (0.0.0.0 0.0.0.0): ").strip()
host2_loop = input("Enter loopback address for host2 (0.0.0.0 0.0.0.0): ").strip()

devices = [host1, host2]



def send_commands(shell, ip_address, client):
    enter_key = "\n"
    print(f"Sending commands to host {ip_address}...")
    shell.send(f"terminal length 0 {enter_key}")    

    commands = ['conf t', 'interface loopback1', 'ip address']
    address = host1_loop if (ip_address == host1) else host2_loop

    for command in commands:
        if 'address' in command:
            shell.send(f'{command} {address} {enter_key}')
        else:
            shell.send(f'{command}{enter_key}')


    shell.send(f'end {enter_key}')
    shell.send(f'show ip int bri {enter_key}')

    time.sleep(2)
    router_output = shell.recv(10000).decode("utf-8")
    print(router_output)

    session_active = client.get_transport().is_active()
    if session_active:
        print(f"Closing session for host {ip_address}")
        client.close()
    return router_output

#Build Shell
def build_shell(client, ip_address):
    print(f"Building shell for host {ip_address}...")
    time.sleep(2)
    command_shell = client.invoke_shell()
    print(f"Shell successfully build for host {ip_address}!")    
    
    #Send commands to shell
    send_commands(command_shell, ip_address, client)  
    return


#Connect To Host
def connect_to_host(client, device_info):
    print(f"Connecting to host {device_info['hostname']}...")
    time.sleep(2)
    client.connect(**device_info)
    
    # Build shell
    build_shell(client, device_info['hostname'])
    return
            
        


# Build SSH Client    
def build_ssh_client(ip_address, username='admin', pt=22, allow_Ag=False, get_Keys=False):
    print(f"Building ssh_client for host {ip_address}...")
    time.sleep(2)
    
    device_info ={      
            "hostname": f"{ip_address}",
            "username": f"{username}",
            "port": f"{pt}",
            "password": f"{pwd}",
            "allow_agent": f"{allow_Ag}",
            "look_for_keys": f"{get_Keys}"  
        }
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connect_to_host(ssh_client, device_info)  

    return

for address in devices:
    build_ssh_client(address)

