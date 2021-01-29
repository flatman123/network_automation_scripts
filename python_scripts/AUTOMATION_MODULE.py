import paramiko
import time


def build_ssh(host):
    print(f'Generating ssh client for host {host}...')
    time.sleep(3)
    ssh_client = paramiko.SSHClient()
    return ssh_client

def connect_to_host(client, host_ip, user, pwd, server_port='22', allow_agnt=False, keys=False ):
    # print( host_ip, user, pwd, server_port, allow_agnt, keys)
    print(f'Connecting client to {host_ip}...')
    time.sleep(3)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_ip, port=server_port, username=user,
                    password=pwd, allow_agent=allow_agnt, look_for_keys=keys)
    print(f'Successfully connected to {host_ip}!')
    return client

def build_shell(client, host):
    print(f'Building shell {host}...')
    time.sleep(3)
    client_shell = client.invoke_shell()
    return client_shell

def close_session(client_shell):
    shell_is_active = client_shell.get_transport().is_active()
    if shell_is_active:
        print(f'Closing ssh session..')
        time.sleep(3)
        client_shell.close()
        print('Session Closed')
    return

def send_commands(client_shell, commands, enter='\n', timeout=5):
    print('Sending commands to device...')

    ''' UNCOMMENT THIS LINE IF YOU'RE WORKING WITH A CISCO DEVICE'''
    client_shell.send(f'terminal length 0 {enter}')

    client_shell.send(f'{commands}{enter}')
    time.sleep(timeout)
    output = client_shell.recv(10000).decode('utf-8')
    close_session(client_shell)
    return output


host_ip = '192.168.0.178'
usr = 'admin'
pwd = 'cisco123'
port = '22'

device_info = {
    'host_ip': host_ip,
    'user': usr,
    'pwd': pwd,
    'server_port': port
}

if __name__ == '__main__':
    client = build_ssh()
    connect = connect_to_host(client, **device_info)
    shell = build_shell(client)
    commands = 'enable, show ip int bri'.split(',')
    for cmd in commands:
        results = send_commands(shell, cmd)
    print(results)
    close_session(client)
