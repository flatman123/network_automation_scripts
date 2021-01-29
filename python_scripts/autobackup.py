import time
import deviceo
import datetime
import concurrent

t1 = time.perf_counter()

def autobackup(ip_address):
    # todays_date = datetime.datetime().now()

    ip_address = f'{ip_address}'
    client = deviceo.build_ssh_client(ip_address)
    connect = deviceo.connect_to_client(client, ip_address, 'admin', 'cisco123')
    shell = deviceo.build_shell(client, ip_address)
    
    cmd_out = deviceo.send_commands(shell, 'show run').split('\n')
    
    configuration = cmd_out[7:-1]

    print(f'Backing up configuration for host {ip_address}..')
    with open(f'{ip_address}_backup_config.txt', 'w') as file1:
        for line in configuration:
            file1.write(line)
    return

#This context manager is needed  for threading
with concurrent.futures.ThreadPoolExecutor() as executor:
    host_octects = [
        '192.168.0.240',
        '192.168.0.166', 
        '192.168.0.242',
        '192.168.0.198',
        '192.168.0.191',
        '172.8.4.8',
        '172.5.9.2',
        '172.16.17.6',
        '172.10.10.4'
        ]
    executor.map(autobackup, host_octects)


t2 = time.perf_counter()
print(f'Script finished running in {t2-t1} seconds.')

# if __name__ == "__main__":
#     #This context manager is needed  for threading
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         host_octects = ['240', '166', '242','123', '198','191','167','172.8.4.8','172.5.9.2']
#         executor.map(autobackup, host_octects)