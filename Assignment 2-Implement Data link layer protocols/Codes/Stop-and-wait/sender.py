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

# _________________________________________________________________#
# getting the dataframes
# _________________________________________________________________#
# get values to send
m = ["1010", "101011", "10101111", "1100", "1010110101", "10101101"]
print("Data which is being sent : ", m)

# apply CRC to all
polynomial = '1011'

message = []
for i in range(0, len(m)):
    message.append(CRCutil(m[i], polynomial))

# generate data frames to send
message = packets(message)

# _________________________________________________________________#
# length of the array
f = str(len(message))
conn.send(f.encode())
f = int(f)
print("\n<------------------------------------------------------------>")

while True:
    counter = 0
    while counter < f:
        # send the dataframe
        conn.send(message[counter])
        # set timeout
        conn.settimeout(3)
        try:
            ack = conn.recv(1518)
            ack = ack.decode()
        except socket.timeout:
            print("||------------->Timeout!")
            ack = "1"
        if ack != "1":
            print("||------------->ACK received!")
            counter = counter + 1
            time.sleep(1)
        else:
            print("||------------->Resending........")
            time.sleep(1)

    # Closing Connection
    conn.close()
    print("\n<---------------------Connection Closed--------------------->")
    break
