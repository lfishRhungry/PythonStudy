# coding: utf-8
# Port scanner with multiple threads. (threading pool)

import socket
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

socket.setdefaulttimeout(0.5)
ports = [ i for i in range(1, 1025)]  # number of port

print('-' * 60)
remote_server = input("Enter a remote host or IP address to scan:\n")
remote_server_ip = socket.gethostbyname(remote_server)

print('-' * 60)
print('Please wait, scanning remote host ', remote_server_ip)
print('-' * 60)

# scanning function that scans only one port
def scan(port):
    try:
        with socket.socket(2, 1) as s:
            res = s.connect_ex((remote_server_ip, port))
            if res == 0:
                print('Port {}: OPEN'.format(port))
    except Exception as e:
        print(e)

# Check what time the scan started
t1 = datetime.now()
# set the number of threads in pool
# default parameter is the number of kernels
pool = ThreadPool()
pool.map(scan, ports)
pool.close()
pool.join()  # wait for sub-thread ending

print('Multiprocess Scanning Completed in  ', datetime.now() - t1)