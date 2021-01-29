import paramiko
import time

# routers  0.182, 0.114, 0.138

def get_config(file):
    with open(file) as rtr_config_file:
        read_file = rtr_config_file.readlines()
    return read_file


def router_auto_config():
    router_octets = [
        ('130', 'jeffmci'),
        # ('178', 'admin'),
        # ('104', 'admin')
    ]
    pwd = 'cisco123'

    for value in router_octets:
        print(f'connecting to Router at 192.168.0.{value[0]}')
        router_defaults = {
            'hostname': f'192.168.0.{value[0]}',
            'username': f'{value[1]}',
            'password': pwd,
            'port': '22',
            'allow_agent': False,
            'look_for_keys': False
        }
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(**router_defaults)

        command_shell = ssh_client.invoke_shell()
        print('Fetching configuration file...')
        # FETCH CONFIGURATION FILE
        config_file = get_config('Links_commands.txt')

        print(f'Configuring Router 192.168.0.{value[0]}')

        for line in config_file:
            command_shell.send(line)
            time.sleep(5)

        output = command_shell.recv(10000)
        session_is_active = ssh_client.get_transport().is_active()

        print(f'OUTPUT: {output.decode("utf-8")}')
        if session_is_active:
            ssh_client.close()
    return

router_auto_config()






