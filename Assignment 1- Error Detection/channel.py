# converts the codeword to k dataword of size n and store it to a file
def getDword(b, div):
    codeword = []
    for x in range(0, len(b), div):
        codeword.append(b[x:x + div])
        x = x + div

    with open('SharedMemory.txt', 'w') as f:
        for info in range(0, len(codeword)):
            f.writelines(codeword[info] + '\n')
# get the full message in a file
def getFullMsg(filename):
    f = open(filename, 'r')
    codeword = f.read()
    return codeword
# read the datawords from file and append it to a list
def readMsg():
    f = open('SharedMemory.txt', 'r')
    datawords = []
    for items in f:
        datawords.append(items.strip())  # removes the newlines
    return datawords
# write the values of list into data.txt
def writeMsg(L):
    with open('data.txt', 'w') as f:
        for i in range(0, len(L)):
            f.write(L[i])
# inject error to the codeword
def injectError():
    with open('data.txt', 'r') as f:
        L = f.read()
    print("SIZE OF THE CODEWORD IS : " + str(len(L)))
    print("TYPE OF ERRORS TO CHOOSE :\n1.PRESS 1 FOR BIT ERROR \n2.PRESS 2 FOR BURST ERROR")
    t = int(input())
    if t == 1:
        print("INJECT ERROR IN POSITION OF YOUR CHOICE (RANGE IS => [0,Size-1] ) : ")
        i = int(input())
        if L[i] == '0':
            L = L[:i] + '1' + L[i + 1:]
        else:
            L = L[:i] + '0' + L[i + 1:]
    elif t == 2:
        print("TOTAL NO OF ERRORS TO INJECT (IN BOUND) : ")
        n = int(input())
        for x in range(n):
            print("INJECT ERROR IN POSITION OF YOUR CHOICE (RANGE IS => [0,Size-1]) : ")
            i = int(input())
            if L[i] == '0':
                L = L[:i] + '1' + L[i + 1:]
            else:
                L = L[:i] + '0' + L[i + 1:]
    else:
        print("NO ERRORS INJECTED ")
    writeMsg(L)