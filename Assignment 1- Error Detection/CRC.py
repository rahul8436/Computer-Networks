from channel import getDword, readMsg, writeMsg, getFullMsg, injectError
import sys
# CRC --> Cyclic Redundancy Check
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
    div = len(polynomial) # div --> length of polynomial
    temp = codeword[0: div] # from '0' to div-1 (storing temporarily)
    while div < len(codeword):
        if temp[0] == '1':
            temp = XOR(polynomial, temp) + codeword[div]
        else:
            temp = XOR('0' * div, temp) + codeword[div]
        div += 1
    # for getting remainder
    # For the last n bits, we have to carry it out
    # normally as increased value of pick will cause Index Out of Bounds.
    if temp[0] == '1':
        temp = XOR(polynomial, temp)
    else:
        temp = XOR('0' * div, temp)
    return temp
# returns the codeword with redundent bits
def CRCutil(data, polynomial):
    l = len(polynomial)
    codeword = data + '0' * (l - 1)
    remainder = CRC(codeword, polynomial)
    codeword = data + remainder
    return codeword
def CRCcheck(data, polynomial):
    l = len(polynomial)  # l --> length of  divisor
    codeword = data + '0' * (l - 1)  # l-1 no of zeroes are being added with actual data
    remainder = CRC(codeword, polynomial)
    flag = 1
    for i in range(0, len(remainder)):
        if remainder[i] == '1':
            flag = 0
            break
    if flag == 1:
        print(">> Remainder : " + remainder)
        print(">> No Error Detected!")
        print("\n>>PASSED")
    else:
        print(">> Remainder : " + remainder)
        print(">> Corrupted data received!")
        print("\n>>FAILED")
if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        codeword = f.read()
    # get the dataword
    print("Data : " + codeword)
    print("\n")
    print("--------------SENDER----------------\n")
    polynomial = '111010101'    #CRC-8-ATM
    # create the codeword with remainder using CRC
    codeword = CRCutil(codeword, polynomial)
    # write the message to data.txt
    writeMsg(codeword)
    print(">>Sending.....\n")
    print("IF YOU WANT TO INJECT ERRORS PRESS 'y' ELSE PRESS 'n' ")
    eflag = input()
    if eflag == 'y':
        injectError()
    else:
        print("NO ERROR IS INJECTED")
    print("\nDATA HAS BEEN PASSED TO RECEIVER SIDE SUCCESSFULLY\n")
    print("PRESS r TO ENTER TO RECEIVER SIDE:")
    flag = input()
    if flag == 'r':
        print("\n--------------RECEIVER----------------")
    else:
        print("HAPPY CODING!!!!")
        exit()
    print("RECEIVED MESSAGE IS : ")
    rCodeword = getFullMsg('data.txt')  # received codeword
    print(rCodeword)
    # validate the data
    CRCcheck(rCodeword, polynomial)  # validate at the receiver side
    print("\n")