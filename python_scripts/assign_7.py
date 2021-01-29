import paramiko
import datetime
import time
import getpass
import sys
import concurrent.futures

#THIS SCRIPT WILL PULL COMMANDS FROM USER AND SAVE OUTPUT TO LOCAL MACHINE.

pwd = getpass.getpass(prompt='Enter password: '.strip(), stream=sys.stderr)
enter = '\n'
commands = input(f"Enter your commands (please separate by commas(','): ").strip().split(',')

# def backup_config():

def send_commands(shell_client, cmds, line_break=enter):
    print('Building sending commands...')
    time.sleep(1)
    shell_client.send(f'terminal length 0{line_break}')
    for line in cmds:
        shell_client.send(line + line_break)
        time.sleep(2)
    output = shell_client.recv(10000).decode('utf-8')
    return output


def build_shell(client):
    print('Building shell...')
    time.sleep(2)
    shell = client.invoke_shell()

    #Send commands
    output = send_commands(shell, commands)
    return output

def connect_to_client(client, device):
    print(f"Connecting to host {device['hostname']}...")
    time.sleep(1)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connected to host {device['hostname']}!!")
    client.connect(**device)
    session_active = client.get_transport().is_active()
    return session_active

def save_to_file(config, host):
    todays_date = datetime.datetime.now()
    year = todays_date.year
    month = todays_date.month
    day = todays_date.day

    print(f'Saving data to file for {host}...')
    time.sleep(1)

    with open(f"{host}-{month}-{day}-{year}.txt", 'w') as output_File:
        for line in config:
            output_File.write(line)

    print(f'file for host {host}, built!')
    return

def build_ssh_client(octet):
    print(f"Setting up ssh client for host 192.168.0.{octet}...")
    time.sleep(1)
    device_info = {
            'hostname': f'192.168.0.{octet}',
            'port': 22,
            'username': 'admin',
            'password': pwd,
            'allow_agent': False,
            'look_for_keys': False
        }
    ssh_client = paramiko.SSHClient()

    #connect to client
    session_active = connect_to_client(ssh_client, device_info)
    #build shell
    output = build_shell(ssh_client)

    #save to file
    save_to_file(output, device_info['hostname'])
    return [output, session_active]

# THREADING

with concurrent.futures.ThreadPoolExecutor() as executor:
    octets = ['191', '242']
    #compile threads
    results = executor.map(build_ssh_client, octets)

