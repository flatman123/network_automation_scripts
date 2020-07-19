import myPymodule
import time

host_ip = '192.168.0.104'
usr = 'admin'
pwd = 'cisco123'
port = '22'

device_info = {
    'host_ip': host_ip,
    'user': usr,
    'pwd': pwd,
    'server_port': port
}

ssh_client = myPymodule.build_ssh()
connect = myPymodule.connect_to_host(ssh_client, **device_info)
shell = myPymodule.build_shell(ssh_client)
configuration_output = myPymodule.send_commands(shell, 'show run')\
                                .splitlines()\

configuration_file = '\n'.join(configuration_output[7:-1])

myPymodule.close_session(ssh_client)

def backup_config(file):
    print(f'Backing up configuration for host {host_ip}...')
    time.sleep(3)
    with open(f'{host_ip}_RTR_config.txt', 'w') as config_file:
        config_file.write(file)
    time.sleep(3)
    print(f'Backup completed!')
    return

backup_config(configuration_file)

