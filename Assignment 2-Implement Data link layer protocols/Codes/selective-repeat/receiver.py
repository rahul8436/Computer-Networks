import time
import socket
import random
from channel import unpacker, injectError, CRCcheck

# ESTABLISHING CONNECTION
s = socket.socket()
host1 = socket.gethostname()
ip = socket.gethostbyname(host1)

host = str(ip)

port = 8000
name = '<-----------------------------WELCOME TO SENDER STATION-------------------------->'

# Connect to remote ADDRESS, and then wraps the connection in an SSL channel
s.connect((host, port))

s.send(name.encode())
s_name = s.recv(1518)
s_name = s_name.decode()

print("\n", s_name)

# _____________________________________________________________________#

f = s.recv(1518)
f = f.decode()
f = int(f)

n = s.recv(1518)
n = n.decode()
n = int(n)

while True:
    buffer = []
    message = []

    polynomial = '1011'
    # create a buffer to store data temporarily
    for x in range(0, n):
        buffer.append('0')

    for j in range(0, n):
        time.sleep(1)
        temp = s.recv(1518)
        temp = unpacker(temp)
        buffer[j] = temp
        time.sleep(1)

    i = n
    counter = 0
    time1 = time.time()
    TIMEOUT = 3
    switch = 0
    while counter < f:
        # send ack for correct data frame and nack for incorrect data frame
        # 0 denotes no error 1 denotes error
        # error = random.randint(0,1)
        # Check CRC
        valid = injectError(buffer[counter % n])
        error = CRCcheck(valid, polynomial)
        # ----> 1 represent error and 0 represent no error <----#
        e = str(error)
        # send the ack

        # random time delay <-------------------------------------->
        a = random.randint(0, 4)
        time.sleep(a)
        print("Time: ", a)
        # <-------------------------------------------------------->
        # if timeout happens nothing is being sent
        if a < 3:
            s.send(e.encode())
        else:
            error = 1

        # collect the message from buffer
        if a < 3:
            if error != 1:
                message.append(valid[:-3])

        # as nothing being sent we have to ignore the previous message sent

        if i < f:
            switch = 0
        else:
            switch = 1
        # receiver
        temp1 = s.recv(1518)
        temp1 = unpacker(temp1)
        # print(temp1)
        # validate remaining ack
        if switch == 1:
            if error != 1:
                counter = counter + 1
            else:
                buffer[counter % n] = temp1

        if switch == 0:
            # receive the dataframe
            if error != 1:
                # reorganize the buffer
                x = 0
                for x in range(0, n - 1):
                    buffer[x] = buffer[x + 1]
                buffer[n - 1] = temp1
                i = i + 1
                counter = counter + 1

            else:
                # correct the values in buffer
                buffer[counter % n] = temp1
    s.close()
    print("<----------------------------------CONNECTION CLOSED------------------------------------>")
    break