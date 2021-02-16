import sys

def createExec(file = 'a.out'):
    data = open(file, 'rb').read()
    nd = []
    cc = 0
    while data[cc] != 0xff:
        cc += 1
    while data[cc] != None:
        nd.append(data[cc])
        cc += 1
        try:
            data[cc]
        except IndexError:
            cc -= 1
            break
    return bytearray(nd[1:])

if __name__ == "__main__":
    open(sys.argv[2], 'wb').write(createExec(sys.argv[1]))