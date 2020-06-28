import csv
import random

with open('./device_info.csv','a') as csvFile:
    HEADERS = ['IPADDRESS', 'DEVICE', 'USERNAME']
    DEVICES = ['Cisco', 'Juniper', 'SonicWall']
    IP_ADDRESS_PREFIX = '192.168.0.'

    write_info = csv.writer(csvFile)
    write_info.writerow(HEADERS)

    for octet in range(1,60):
        random_device = random.randint(0, len(DEVICES))
        device_info = f'192.168.0.{octet}, {DEVICES[random_device - 1]}, admin'.split(',')
        write_info.writerow(device_info)
        
