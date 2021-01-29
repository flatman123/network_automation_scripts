import paramiko
import time

# routers  0.182, 0.114, 0.138

def get_config(file):
    with open(file) as rtr_config_file:
        read_file = rtr_config_file.readlines()
    return read_file


def router_auto_config():
    router_octets = [
        ('182', 'admin2'),
        ('114', 'admin'),
        ('138', 'admin')
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

        # FETCH CONFIGURATION FILE
        config_file = get_config('ROUTER_DEFAULTS_CONFIG.txt')

        for line in config_file:
            command_shell.send(line)
            time.sleep(3)

        session_is_active = ssh_client.get_transport().is_active()
        output = command_shell.recv(10000).decode('utf-8')

        print(output)
        if session_is_active:
            ssh_client.close()
    return

router_auto_config()






