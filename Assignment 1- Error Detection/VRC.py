from channel import getDword, readMsg, writeMsg, getFullMsg, injectError
import sys
# VRC --> Vertical Redundancy Check
def VRC(dataword):
    oneCount = 0
    for ones in dataword:
        if ones == '1':
            oneCount = oneCount + 1
    # Even and Odd Parity Checker
    if oneCount % 2 == 0:
        dataword = dataword + '0'
    else:
        dataword = dataword + '1'
    return dataword
def VRCutil(L):
    for i in range(len(L)):
        L[i] = VRC(L[i])  #odd even --> calling the vrc fn for every databit
    return L
# check the dataword if it is valid or not
def VRCparity(dataword):
    oneCount = 0
    for ones in dataword:
        if ones == '1':
            oneCount = oneCount + 1
    if oneCount % 2 == 0:
        print("Data Accepted! --> PASSED")
    else:
        print("Received Data seems to be Corrupted: --> FAILED")
def VRCcheck(L):
    for i in range(len(L)):
        VRCparity(L[i])
if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        codeward = f.read()
    # size of each dataword
    print("--------------SENDER----------------")
    print("\nENTER THE SIZE OF EACH DATAWORD:")
    div = int(input())
    print("\n")
    # read the codeword and break it into dataword
    getDword(codeward, div) #div --> size of each data frame
    # collect the dataword into a list
    L = readMsg()
    # VRC and send codeword
    L = VRCutil(L)
    # write the message to data.txt
    writeMsg(L)
    print(">>Sending........\n")
    print("IF YOU WANT TO INJECT ERRORS PRESS 'y' ELSE PRESS 'n' ")
    eflag = input()
    if eflag == 'y':
        injectError()
    else:
        print("NO ERROR IS INJECTED ")
    print("\nDATA HAS BEEN PASSED TO RECEIVER SIDE SUCCESSFULLY\n")
    print("PRESS r TO ENTER TO RECEIVER SIDE:")
    flag = input()
    print("\nloading.......\n")
    if flag == 'r':
        print("\n--------------RECEIVER----------------")
    else:
        print("THANK YOU,HAPPY CODING :)")
        exit()
    print("RECEIVED MESSAGE IS : ")
    rCodeword = getFullMsg('data.txt')  # received codeword
    print(rCodeword)
    # VRC and check
    getDword(rCodeword, div + 1)  # read the codeword and break it into dataword
    rL = readMsg()  # store into list
    print("\n")
    VRCcheck(rL)  # validate at the receiver side