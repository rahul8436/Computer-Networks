import time
import socket
import random
from channel import unpacker, injectError, CRCcheck

# Establishing Connection
s = socket.socket()
host1 = socket.gethostname()
ip = socket.gethostbyname(host1)
host = str(ip)
port = 8000
name = '<-----------------------------WELCOME TO RECEIVER STATION-------------------------->'
# Connect to remote ADDR, and then wraps the connection in an SSL channel
s.connect((host, port))
s.send(name.encode())
s_name = s.recv(1518)
s_name = s_name.decode()
print(s_name)
# Sender end Connection
f = s.recv(1518)
f = f.decode()
f = int(f)

while True:
    counter = 0
    message = []
    polynomial = '1011'
    while counter < f:
        # receive the data packet
        temp = s.recv(1518)
        temp = unpacker(temp)
        # Injecting error
        temp = injectError(temp)
        # Data Validation
        error = CRCcheck(temp, polynomial)
        # random time delay
        a = random.randint(0, 4)
        time.sleep(a)
        print("Time Delay Encountered is: ", a)
        # 0 for error and 1 for no error
        e = str(error)
        # if timeout happens nothing is being sent
        if a < 3:
            s.send(e.encode())
        else:
            error = 1
        if a < 3:
            if e != "1":
                print("\n>>Partition Received is :", temp[:-3], "\n")
                counter = counter + 1
    # Closing Connection
    s.close()
    print("\n<---------------------Connection Closed--------------------->")
    break
