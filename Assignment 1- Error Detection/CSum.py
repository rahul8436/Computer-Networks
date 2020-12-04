from channel import getDword, readMsg, writeMsg, getFullMsg, injectError
import sys
# checkSum
# function to add two binary numbers for checkSum
def binSum(bn1, bn2, div):
    s1 = bin(int(bn1, 2) + int(bn2, 2))
    if len(s1) == div + 3:
        carry = '1'
        s2 = s1[3:]
        s1 = binSum(s2, carry, div)
        return s1
    else:
        return s1[2:]
# get the checkSum
def CheckSum(L, div):
    temp = L[0]
    for i in range(len(L) - 1):
        temp = binSum(temp, L[i + 1], div)
        # for attaining same length
        if len(temp) != div:
            for i in range(div - len(temp)):
                temp = '0' + temp
    checkSum = temp
    # making 1's complement
    for i in range(len(checkSum)):
        if checkSum[i] == '0':
            checkSum = checkSum[:i] + '1' + checkSum[i + 1:]
        else:
            checkSum = checkSum[:i] + '0' + checkSum[i + 1:]
    return checkSum
def CSutil(L, div):
    csum = CheckSum(L, div)
    L.append(csum) #appending checksum value to actual list
    return L
def CScheck(L, div):
    csum = CheckSum(L, div)
    flag = 0
    for i in range(len(csum)):
        if csum[i] == '1':
            flag = 1
            break
    for i in range(len(csum)):
        if csum[i] == '0':
            csum = csum[:i] + '1' + csum[i + 1:]
        else:
            csum = csum[:i] + '0' + csum[i + 1:]
    if flag == 0:
        print(">> checksum : " + csum)
        print("\n>> Data accepted! No error found!")
        print("\nPASSED")
    else:
        print(">> checksum : " + csum)
        print("\n>> Error Detected in data!")
        print("\nFAILED")
if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        codeward = f.read()
    # size of each dataword
    print("--------------SENDER----------------")
    print("\nENTER THE SIZE OF THE DATAWORD :")
    div = int(input())
    print("\n")
    # creating dataword of size div (breaking the codewords)
    getDword(codeward, div)
    L = readMsg()  # read the codeword and break it into dataword and add it to a list
    # CheckSum and append the redundancy bits
    L = CSutil(L, div)
    # write the message to data.txt
    writeMsg(L)
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
    # CheckSum and check
    # read the codeword and break it into dataword
    getDword(rCodeword, div)
    # store the values in list
    rL = readMsg()
    print("\n")
    CScheck(rL, div)  # validate at the receiver side