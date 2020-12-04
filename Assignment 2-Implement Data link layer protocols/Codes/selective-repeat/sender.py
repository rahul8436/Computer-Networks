import socket
import time
from channel import packets, CRCutil

# Establishing Connection
s = socket.socket()
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 8000
s.bind((host, port))
name = '<-----------------------------WELCOME TO SENDER STATION-------------------------->'
# Receiver End Connection
s.listen(1)
print("\nConnecting.........................\n")
# get the socket object and address info from the receiver end
conn, addr = s.accept()
print("Connected to ---->", addr[0], "(", addr[1], ")")
# buffer size = 1518
s_name = conn.recv(1518)
s_name = s_name.decode()
print("\n", s_name)
conn.send(name.encode())

'Get the dataframes'
# _________________________________________________________________#
# get values to send
m = ["1010", "101011", "10101111", "1100", "1010110101", "10101101"]
print(m)

# apply CRC to all
polynomial = '1011'

message = []
for i in range(0, len(m)):
    message.append(CRCutil(m[i], polynomial))

# generate data frames to send
message = packets(message)

# _________________________________________________________________#

f = str(len(message))  # length of the array
conn.send(f.encode())
f = int(f)

print("Enter the size of the sliding window : ")
n = input()
conn.send(n.encode())
n = int(n)


while True:
    'In selective repeat only the lost data frames are retransmitted'
    # First dataframes are transmitted before receiving an ack
    for j in range(0, n):
        time.sleep(1)
        # print(time.time())
        conn.send(message[j])
        print("||------------------->Sending")
        time.sleep(1)
    i = n
    counter = 0  # acknowledgement counter
    TIMEOUT = 3

    switch = 0
    hpass = 0
    holder = message[0]
    while counter < f:
        # receive ack signals
        # time1 = time.time()
        conn.settimeout(3)
        try:
            ack = conn.recv(1518)
            ack = ack.decode()
        except socket.timeout:
            print("||------------------->Timeout Error")
            ack = "1"

        if i < f:
            switch = 0
        else:
            switch = 1
        # only ack left
        if switch == 1:
            if ack != "1":
                print("\n||------------------->ACK NO ", counter)
                print("\n")
                time.sleep(1)
                a = message[counter]
                holder = a
                counter = counter + 1
            else:
                # for nack
                print("\n||------------------->NACK NO ", counter)
                print("||------------------->Resending the frame ", counter, "\n")
                time.sleep(1)
                holder = message[counter]
        if switch == 0:
            # transmit the next dataframe
            if ack != "1":
                print("\n||------------------->ACK NO ", counter)
                print("||------------------->Sending the next frame...", (counter + n), "\n")
                time.sleep(1)
                holder = message[i]
                i = i + 1
                counter = counter + 1
            else:
                print("\n||------------------->NACK NO ", counter)
                print("||------------------->Resending the data packet ", counter, "\n")
                time.sleep(1)
                holder = message[counter]
        conn.send(holder)

    conn.close()
    print("<----------------------------------CONNECTION CLOSED------------------------------------>")
    break
