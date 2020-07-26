import myPymodule
import datetime
import time

last_octet = ['184', '186', '110']

def backup_multiple_devices(devices):
    todays_date = datetime.datetime.now()
    month = todays_date.month
    day = todays_date.day
    year = todays_date.year

    if len(last_octet) > 0:
        for octet in last_octet:
            host_info = {
                'hostname': f'192.168.0.{octet}',
                'username': 'admin',
                'pwd': 'cisco123',
                'port': '22',
            }
            ssh_client = myPymodule.build_ssh(host_info['hostname'])
            connect = myPymodule.connect_to_host(ssh_client,
                                                 host_info['hostname'],
                                                 host_info['username'],
                                                 host_info['pwd'],
                                                 host_info['port'])
            shell = myPymodule.build_shell(ssh_client, host_info['hostname'])
            get_configuration = myPymodule.send_commands(shell, 'show run').splitlines()
            configuration_output = '\n'.join(get_configuration[7:-1])

            with open(f'{host_info["hostname"]}_{month}-{day}-{year}_backup.txt', 'w') as backup_file:
                time.sleep(2)
                print(f'Backing up configuration for host {host_info["hostname"]}...')
                backup_file.write(configuration_output)

            print(f'Backup for device at {host_info["hostname"]} complete!')
            time.sleep(4)
    return

backup_multiple_devices(last_octet)







