from channel import getDword, readMsg, writeMsg, getFullMsg, injectError
import sys
# LRC -->Longitudinal Redundancy Check
def LRC(L):
    rbit = []
    oneCount = 0
    for i in range(len(L[0])):
        oneCount = 0
        for j in range(len(L)):
            if L[j][i] == '1':
                oneCount += 1
        if oneCount % 2 == 0:
            rbit.append('0')
        else:
            rbit.append('1')
    return rbit
#utility fn for lrc
def LRCutil(L):
    rbits = LRC(L)
    separator = ''
    rb = separator.join(rbits)
    L.append(rb)
    return L
# to validate LRC at the receiver side
def LRCcheck(L):
    oneCount = 0
    flag = 0
    for i in range(len(L[0])):
        oneCount = 0
        for j in range(len(L)):
            if L[j][i] == '1':
                oneCount += 1
        if oneCount % 2 == 0:
            # if even parity data is valid
            print("DATA AT COLUMN NO --> " + str(i) + " : ACCEPTED !")
        else:
            print("CORRUPTED DATA AT COLUMN NO --> " + str(i) + " : REJECTED !")
            flag = 1

    if flag == 1:
        print("\n>> Error Detected in the data!")
        print("\nFAILED")
    else:
        print("\n>> No error detected! Data accepted!")
        print("\nPASSED")
if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        codeward = f.read()
    # size of each dataword
    print("--------------SENDER----------------")
    print("\nENTER THE SIZE OF EACH DATAWORD:")
    div = int(input())
    print("\n")
    # creating dataword of size div
    getDword(codeward, div)
    L = readMsg()  # read the codeword and break it into dataword and add it to a list
    # LRC and append the redundancy bits
    L = LRCutil(L)
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
    print("PRESS r TO ENTER TO RECEIVER SIDE ELSE PRESS ANY KEY TO GET OUT:")
    flag = input()
    print("\nloading.......\n")
    if flag == 'r':
        print("\n--------------RECEIVER----------------")
    else:
        print("HAPPY CODING!!!!")
        exit()
    print("RECEIVED MESSAGE IS : ")
    rCodeword = getFullMsg('data.txt')  # received codeword
    print(rCodeword)
    # LRC and check
    # read the codeword and break it into dataword
    getDword(rCodeword, div)
    # store the values in list
    rL = readMsg()
    print("\n")
    LRCcheck(rL)  # validate at the receiver side