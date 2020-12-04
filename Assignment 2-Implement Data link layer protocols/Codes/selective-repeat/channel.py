import struct
import random


def decimalToBinary(n):
    return n.replace("0b", "")


def binarycode(s):
    a_byte_array = bytearray(s, "utf8")

    byte_list = []

    for byte in a_byte_array:
        binary_representation = bin(byte)
        byte_list.append(decimalToBinary(binary_representation))
    return byte_list


# <----------------------CRC---------------------------->
# ERROR DETECTION
# polynomial = '1011' #CRC-4
# cyclic redundancy check
# XOR function for binary division

def XOR(a, b):
    result = []
    separator = ''
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return separator.join(result)


# CRC function which peforms binary division and returns the remainder

def CRC(codeword, polynomial):
    div = len(polynomial)
    temp = codeword[0: div]

    while div < len(codeword):
        if temp[0] == '1':
            temp = XOR(polynomial, temp) + codeword[div]
        else:
            temp = XOR('0' * div, temp) + codeword[div]

        div += 1
    if temp[0] == '1':
        temp = XOR(polynomial, temp)
    else:
        temp = XOR('0' * div, temp)

    return temp


# returns the codeword with redundant bits
def CRCutil(data, polynomial):
    l = len(polynomial)
    codeword = data + '0' * (l - 1)
    remainder = CRC(codeword, polynomial)
    codeword = data + remainder
    return codeword


def CRCcheck(data, polynomial):
    l = len(polynomial)
    codeword = data + '0' * (l - 1)
    remainder = CRC(codeword, polynomial)
    flag = 1
    for i in range(0, len(remainder)):
        if remainder[i] == '1':
            flag = 0
            break

    if flag == 1:
        print(">> Remainder : " + remainder)
        return 0
    else:
        print(">> Remainder : " + remainder)
        return 1


# Error Injection
def injectError(L):
    t = random.randint(0, 7)
    size = len(L)
    if t == 1:
        i = random.randint(0, size - 1)
        if L[i] == '0':
            L = L[:i] + '1' + L[i + 1:]
        else:
            L = L[:i] + '0' + L[i + 1:]
    elif t == 2:
        print("Random Error Injected\n")
        n = random.randint(0, size - 1)
        for x in range(n):
            i = random.randint(0, size - 1)
            if L[i] == '0':
                L = L[:i] + '1' + L[i + 1:]
            else:
                L = L[:i] + '0' + L[i + 1:]
    else:
        print("No Error Injected")
    return L


# <--------------DATA FRAME FORMAT------------->#
# Q limitations--> 8 byte maximum per partition
# Q --> 8 byte
def packet_maker(data):
    premble = "10101010" * 7
    sfd = "10101011"
    # destination address
    da = "11000000" + "10100010" + "00111000" + "00000001"
    # sender address
    sa = "11000000" + "10100010" + "00111000" + "00000001"
    # size of the data
    l = len(data)
    # size
    s = bin(20 + l)[2:]
    s = str(s)
    # data = data + CRC
    # convert it into data packets
    premble = premble + sfd  # (Total 8 bytes)
    # typecasting
    premble = int(premble, 2)
    da = int(da, 2)
    sa = int(sa, 2)
    s = int(s, 2)
    data = int(data, 2)
    # padding done
    return struct.pack('!QQQQQ', premble, da, sa, s, data)


def packets(L):
    s = len(L)
    frames = []
    for i in range(0, s):
        frame = packet_maker(L[i])
        frames.append(frame)
    return frames


def unpacker(data):
    data = struct.unpack('!QQQQQ', data)
    # remove preamble and sfd
    data = data[4]
    data = bin(data)[2:]
    data = str(data)
    return data
