import paramiko
import datetime
import time
import getpass
import concurrent.futures
import sys


# we need variables for public 1 and public2
# we also need tunnel address for both endpoints
# ask for this information ahead of time.

pwd = getpass.getpass(prompt='Enter password: '.strip(), stream=sys.stderr)
pre_shared = getpass.getpass(prompt='Enter password for pre-shared key: '.strip(), stream=sys.stderr)
host_tunnel_address_1 = input('What will the tunnel address be for the first host?(<ADDRESS> <MASK>): ').strip()
host_tunnel_address_2 = input('What will the tunnel address be for the second host?(<ADDRESS> <MASK>): ').strip()
tunnel_source_host1 = "192.168.0.242"
tunnel_source_host2 = "172.10.16.6"

t1 = time.perf_counter()

def placeHolders(line, address):
    holders = {
        "ip address <LOCAL TUNNEL ADDRESS>\n": f"ip address {host_tunnel_address_1 if address == tunnel_source_host1 else host_tunnel_address_2}" ,
        "tunnel source <LOCAL PUBLIC ADDRESS>\n": f"tunnel source {tunnel_source_host1 if address == tunnel_source_host1 else tunnel_source_host2}",
        "tunnel destination <PEER PUBLIC ADDRESS>\n": f"tunnel destination {tunnel_source_host2 if address == tunnel_source_host1 else tunnel_source_host1}",
        "crypto isakmp key 6 <PRE-SHARED> address <PEER ADDRESS>\n": f"crypto isakmp key 6 {pre_shared} address {tunnel_source_host2 if address == tunnel_source_host1 else tunnel_source_host1}",
        "network": f"network {host_tunnel_address_1 if address == tunnel_source_host1 else host_tunnel_address_2} area 13"
    } 
    output = holders.get(line, line)
    return output


#Send Commands
def send_commands(shell, conf_file, address):
    print(f"Sending commands to host {address}...")
    time.sleep(1)
    enter = "\n"
    shell.send(f"terminal length 0{enter}")
    shell.recv(10000)

    with open(f"{conf_file}") as config_file:
        list_comp = [line for line in config_file]
        for line in list_comp:
            config_line = placeHolders(line, address)
            shell.send(config_line + enter)
            time.sleep(1)
    return


#build shell
def build_cmd_shell(client, address):
    print(f"Building shell for host {address}...")
    time.sleep(1)
    shell = client.invoke_shell()
    
    # Send Commands
    send_commands(shell, "gre_ipsec_configuration.txt", address)
    return


# connect client
def connect_to_client(client, device_info, address):
    print(f"Connectin to host {address}...")
    time.sleep(1)
    client.connect(**device_info)
    ssh_session_active = client.get_transport().is_active()
    return ssh_session_active



# build ssh Client
def build_ssh_client(address):
    print(f"Building ssh client for host {address}...")
    time.sleep(1)

    device_info = {
        'hostname': address,
        'port': '22',
        'password': pwd,
        'username': 'admin',
        'allow_agent': False,
        'look_for_keys': False
    }

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connect_to_client(ssh_client, device_info, address)
    build_cmd_shell(ssh_client, address)    

    return ssh_client

with concurrent.futures.ThreadPoolExecutor() as executor:
    hosts = [tunnel_source_host1, tunnel_source_host2]
    threads = executor.map(build_ssh_client, hosts)

t2 = time.perf_counter()

print(f"Script completed in {t2-t1} second(s)")

if __name__ == "__main__":
    #This context manager is needed  for threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        hosts = [tunnel_source_host1, tunnel_source_host2]
        threads = executor.map(build_ssh_client, hosts)
