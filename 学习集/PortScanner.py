# coding: utf-8
# Port scanner with normal method

import socket
from datetime import datetime

# Set time-out to get the scanning fast
socket.setdefaulttimeout(0.5)
print('-' * 60)

remote_server = input("Enter a remote host or IP address to scan:\n")
remote_server_ip = socket.gethostbyname(remote_server)

print('-' * 60)
print('Please wait, scanning remote host ', remote_server_ip)
print('-' * 60)

# Check what time the scan started
t1 = datetime.now()
# put in some error handling for catching errors
try:
    for port in range(1,1025):
        with socket.socket(2,1) as sock: # 2:socket.AF_INET 1:socket.SOCK_STREAM
            res = sock.connect_ex((remote_server_ip,port))
            if res == 0:
                print('Port {}: OPEN'.format(port))
except socket.gaierror:
    print('Hostname could not be resolved.Exiting')
except socket.error:
    print("Could't connect to the server")

# Print the info to screen
print('Scanning Completed in: ', datetime.now() - t1)