import myPymodule

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

myPymodule.send_commands(shell, 'enable')
output = myPymodule.send_commands(shell, 'show ip int bri')

print(output)

myPymodule.close_session(ssh_client)
