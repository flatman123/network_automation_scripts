with open('./devices.txt', 'r',) as device_file:
    read_file = device_file.read().splitlines()
    my_array: []

    for line in read_file:
        print(line.split(':'))

