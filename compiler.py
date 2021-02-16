import sys

def isnum(d):
    se = '1234567890xabcdef'
    for c in d:
        if not c in se: return False
    return True

def isreg(d) : return d.startswith('R') and isnum(d[1:])
def islabel(d): return d.startswith('.')

def split(d=''):
    data = []
    lines = d.splitlines()
    for line in lines:
        words = line.split()
        data += words
        data.append('\n')
    return data

IS = {
    'addrr': 1, #// a + b
    'addrl': 2, #//  a + 5
    'addll': 3, #// add 5 + 45
    'subrr': 4,
    'subrl': 5,
    'sublr': 6,
    'subll': 7,
    'rshr': 8,
    'rshl': 9,
    'lshr': 10,
    'lshl': 11,
    'incr': 12,
    'incl': 13,
    'decr': 14,
    'decl': 15,
    'xorrr': 16,
    'xorrl': 17,
    'xorll': 18,
    'andrr': 19,
    'andrl': 20,
    'andll': 21,
    'orrr': 22,
    'orrl': 23,
    'orll': 24,
    'norrr': 25,
    'norrl': 26,
    'norll': 27,
    'nandrr': 28,
    'nandrl': 29,
    'nandll': 30,
    'xnorrr': 31,
    'xnorrl': 32,
    'xnorll': 33,
    'notr':  34,
    'notl': 35,
    'mov': 36,
    'imm': 37,
    'lodl': 38,
    'lodr': 39,
    'strrmr': 40,
    'strrr': 41,
    'strrml': 42,
    'strrl': 43,
    'brarl': 44,
    'bral': 45,
    'brar': 46,
    'brcrl': 47,
    'brcl': 48,
    'brcr': 49,
    'bncrl': 50,
    'bncl': 51,
    'bncr': 52,
    'brzrl': 53,
    'brzl': 54,
    'brzr': 55,
    'bnzrl': 56,
    'bnzl': 57,
    'bnzr': 58,
    'brnrl': 59,
    'brnl': 60,
    'brnr': 61,
    'brprl': 62,
    'brpl': 63,
    'brpr': 64,
    'nop': 65,
    'hlt': 0xff,
    'call': 66,
    'calr': 67,
    'ret': 90,
    'pushl': 68,
    'pushr': 69,
    'pop': 70,
    'out': 0xfe,
    'int': 0xfd
}

class Compiler8:
    def __init__(self, code=""):
        self.code = code
        self.tokens = code.split()
        self.cci = -1
        self.cti = 3
        self.output = [0]*256
        self.labels = {}
    def f(self):
        self.cci += 1
        return self.tokens[self.cci]
    def push(self, d):
        self.output[self.cti] = d
        self.cti += 1
    def pc(self):
        nd = []
        for dat in self.output:
            if type(dat) == str:
                nd.append(self.labels[dat] if self.labels[dat] >= 0 else 0)
            else:
                nd.append(dat)
        self.output = nd
        return nd
    def c(self):
        ct = self.f()
        print(ct)
        while ct != None:
            if ct.startswith('/*'):
                d = self.f()
                while d != '*/':
                    d = self.f()
            print(ct)
            
            if ct == 'BITS':
                eqs = self.f()
                if eqs == '>=' or eqs == '==' or eqs == '<=':
                    bits = self.f()
                    if isnum(bits):
                        self.output[0] = int(bits)
            elif ct == 'OUT':
                addr = self.f()
                if isnum(addr):
                    self.push(IS['out'])
                    self.push(int(addr))
            elif ct == 'MINREGS':
                eqs = self.f()
                if eqs == '>=' or eqs == '==' or eqs == '<=':
                    regs = self.f()
                    if isnum(regs):
                        self.output[1] = int(regs)
            elif ct == 'MINRAM':
                eqs = self.f()
                if eqs == '>=' or eqs == '==' or eqs == '<=':
                    ram = self.f()
                    if isnum(regs):
                        self.output[2] = int(ram)
            elif islabel(ct):
                self.labels[ct.strip()] = self.cci-11
            elif ct == 'RSH':
                dest = self.f()
                src = self.f()
                if isreg(dest):
                    if isnum(src):
                        self.push(IS['rshl'])
                        self.push(int(dest[1:])-1)
                        self.push(int(src))
                    elif isreg(src):
                        self.push(IS['rshr'])
                        self.push(int(dest[1:])-1)
                        self.push(int(src[1:])-1)
            elif ct == 'LSH':
                dest = self.f()
                src = self.f()
                if isreg(dest):
                    if isnum(src):
                        self.push(IS['lshl'])
                        self.push(int(dest[1:])-1)
                        self.push(int(src))
                    elif isreg(src):
                        self.push(IS['lshr'])
                        self.push(int(dest[1:])-1)
                        self.push(int(src[1:])-1)
            elif ct == 'BRA':
                dest = self.f()
                if islabel(dest):
                    self.push(IS['bral'])
                    self.push(dest)
                elif isreg(dest):
                    self.push(IS['brar'])
                    self.push(int(dest[1:])-1)
            elif ct == 'IMM':
                dest = self.f()
                src = self.f()
                if isreg(dest) and isnum(src):
                    self.push(IS['imm'])
                    self.push(int(src))
                    self.push(int(dest[1:])-1)
                elif isreg(dest) and islabel(src):
                    self.push(IS['imm'])
                    self.push(src)
                    self.push(int(dest[1:])-1)
                    
            elif ct == 'MOV':
                src = self.f()
                dest = self.f()
                if isreg(src) and isreg(dest):
                    self.push(IS['mov'])
                    self.push(int(src[1:])-1)
                    self.push(int(dest[1:])-1)
                    
            elif ct == 'ADD':
                dest = self.f()
                op1 = self.f()
                op2 = self.f()
                if isreg(dest):
                    if isnum(op1) and isnum(op2):
                        self.push(IS['addll'])
                        self.push(int(dest[1:])-1)
                        self.push(int(op1))
                        self.push(int(op2))
                    elif isreg(op1) and isnum(op2):
                        self.push(IS['addrl'])
                        self.push(int(dest[1:])-1)
                        self.push(int(op1[1:])-1)
                        self.push(int(op2))
                    elif isreg(op1) and isreg(op2):
                        self.push(IS['addrr'])
                        self.push(int(dest[1:])-1)
                        self.push(int(op1[1:])-1)
                        self.push(int(op2[1:])-1)
            elif ct == 'SUB':
                dest = self.f()
                op1 = self.f()
                op2 = self.f()
                print(dest, op1, op2)
                if isreg(dest):
                    if isnum(op1) and isnum(op2):
                        self.push(IS['subll'])
                        self.push(int(dest[1:])-1)
                        self.push(int(op1))
                        self.push(int(op2))
                    elif isreg(op1) and isnum(op2):
                        self.push(IS['subrl'])
                        self.push(int(dest[1:])-1)
                        self.push(int(op1[1:])-1)
                        self.push(int(op2))
                    elif isnum(op1) and isreg(op2):
                        self.push(IS['sublr'])
                        self.push(int(dest[1:])-1)
                        self.push(int(op1))
                        self.push(int(op2[1:])-1)
                    elif isreg(op1) and isreg(op2):
                        self.push(IS['subrr'])
                        self.push(int(dest[1:])-1)
                        self.push(int(op1[1:])-1)
                        self.push(int(op2[1:])-1)
            elif ct == 'HLT':
                self.push(0xff)
            try:
                ct = self.f()
            except IndexError:
                return self.pc(), self.labels

def _format_labels_(data):
    labels = {}
    for i in range(len(data)):
        ct = data[i]
        if type(ct) == str:
            if ct.startswith('r.'):
                labels[ct[1:]] = i-8
    return labels

def generateOffsetTable(labels = {}):
    data = "@place 0\n"
    for label in labels:
        data += f"{label}: @org {labels[label]}\n"
    return data+chr(0xff)

def htd(d=''):
    if d.startswith('0x'):
        return int(d[2:], 16)
    elif d.endswith('h'):
        return int(d[:-1], 16)
    elif isnum(d):
        return int(d)
    
def isstring(d = ''): return d.startswith('"') and d.endswith('"')

class Compiler16:
    def __init__(self, code=""):
        self.code = code
        self.tokens = split(code)
        self.cci = -1
        self.cti = 4
        self.bits = 0
        self.regs = 0
        self.ram = 0
        self.output = [0]*(2**16)
        self.labels = {}
    def f(self):
        self.cci += 1
        return self.tokens[self.cci]
    def fstr(self):
        start = self.f()
        string = ""
        if not start.startswith('"'): return
        else:
            string += start
            while not string.endswith('"'):
                start = self.f()
                string += ' '
                string += start
        return string
    def push(self, d):
        self.output[self.cti] = d
        self.cti += 1
    def pc(self):
        nd = []
        for dat in self.output:
            if type(dat) == str and islabel(dat):
                nd.append((self.labels[dat] >> 8) & 0xff if self.labels[dat] >= 0 else 0)
                nd.append(self.labels[dat] & 0xff if self.labels[dat] >= 0 else 0)
            elif isnum(str(dat)):
                nd.append(dat)
        self.output = nd
        return nd
    def include(self, binary=''):
        self.INCLUDE_OFFSET = 0
        data = open(binary, 'rb').read()
        binaryData = []
        readableData = ''
        cc = 0 
        
        while data[cc] != 0xff:
            readableData += chr(data[cc])
            cc += 1
        while data[cc] != None:
            binaryData.append(data[cc])
            cc += 1
            try:
                data[cc]
            except IndexError:
                cc -= 1
                break
        print('[READED]:', readableData)
        lines = readableData.splitlines()
        place_line = lines[0]
        fwords = place_line.split()
        if fwords[0] == '@place':
            self.INCLUDE_OFFSET = int(fwords[1])
        
        for line in lines[1:]:
            words = line.split(":")
            label = words[0].strip()
            data  = words[1].strip()
            ldata = data.split()[1]
            self.labels[label] = int(ldata)
            print(self.labels)
        bdata = binaryData
        for ff in range(len(bdata)):
            #$print(bdata[ff]) if bdata[ff] else None
            self.output[ff+self.INCLUDE_OFFSET] = bdata[ff]
        print(bdata[190:300])
        print(self.labels)
    def c(self):
        ct = self.f()
        #print(ct)
        while ct != None:
            if ct.startswith('//'):
                d = self.f()
                while d != '\n':
                    d = self.f()
            #print(ct)
            if ct == '@org':
                addr = self.f()
                if isnum(addr):
                    self.cti = htd(addr)
            if ct == 'BITS':
                eqs = self.f()
                if eqs == '>=' or eqs == '==' or eqs == '<=':
                    bits = self.f()
                    if isnum(bits):
                        self.output[0] = htd(bits)
                        self.bits = htd(bits)
            elif ct == 'OUT':
                addr = self.f()
                if isnum(addr):
                    self.push(IS['out'])
                    self.push((htd(addr) >> 8) & 0xff)
                    self.push(htd(addr) & 0xff)
            elif ct == 'INT':
                inte = self.f()
                if isnum(inte):
                    self.push(0xfd)
                    self.push(htd(inte))
            elif ct == 'DW':
                word = self.f()
                if isnum(word):
                    self.push((htd(word) >> 8) & 0xff)
                    self.push(htd(word) & 0xff)
                elif islabel(word):
                    self.push(word)
            elif ct == 'DB':
                byte = self.f()
                if isnum(byte):
                    self.push(htd(byte) & 0xff)
                elif islabel(byte):
                    self.push(byte)
                elif byte.startswith('"') and not byte.endswith('"'):
                    self.cci -= 1
                    data = self.fstr()[1:-1]
                    for ch in data:
                        self.push(ord(ch))
                elif byte.startswith('"') and byte.endswith('"'):
                    data = byte[1:-1]
                    for ch in data:
                        self.push(ord(ch))
            elif ct == 'MINREGS':
                eqs = self.f()
                if eqs == '>=' or eqs == '==' or eqs == '<=':
                    regs = self.f()
                    if isnum(regs):
                        self.output[1] = htd(regs)
                        self.regs = htd(regs)
            elif ct == 'MINRAM':
                eqs = self.f()
                if eqs == '>=' or eqs == '==' or eqs == '<=':
                    ram = self.f()
                    if isnum(regs):
                        #print((int(ram) >> 8) & 0xff)
                        self.output[2] = ((htd(ram) >> 8) & 0xff)
                        self.output[3] = (htd(ram) & 0xff)
                        self.ram = htd(ram)
            elif ct == 'INCLUDE':
                binFile = self.f()
                if binFile.startswith("\"") and binFile.endswith('"'):
                    self.include(binFile[1:-1])
            elif islabel(ct):
                self.push(f'r{ct}')
            elif ct == 'RSH':
                dest = self.f()
                src = self.f()
                if isreg(dest):
                    if isnum(src):
                        self.push(IS['rshl'])
                        self.push(htd(dest[1:])-1)
                        self.push((htd(src) >> 8) & 0xff)
                        self.push(htd(src) & 0xff)
                    elif isreg(src):
                        self.push(IS['rshr'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(src[1:])-1)
            elif ct == 'LSH':
                dest = self.f()
                src = self.f()
                if isreg(dest):
                    if isnum(src):
                        self.push(IS['lshl'])
                        self.push(htd(dest[1:])-1)
                        self.push((htd(src) >> 8) & 0xff)
                        self.push(htd(src) & 0xff)
                    elif isreg(src):
                        self.push(IS['lshr'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(src[1:])-1)
            elif ct == 'CALL':
                dest = self.f()
                if islabel(dest):
                    self.push(IS['call'])
                    self.push(dest)
                elif isreg(dest):
                    self.push(IS['calr'])
                    self.push(htd(dest[1:])-1)
            elif ct == 'RET':
                self.push(IS['ret'])
            elif ct == 'PUSH':
                src = self.f()
                if islabel(src):
                    self.push(IS['pushl'])
                    self.push(src)
                elif isnum(src):
                    self.push(IS['pushl'])
                    self.push((htd(src) >> 8) & 0xff)
                    self.push(htd(src) & 0xff)
                elif isreg(src):
                    self.push(IS['pushr'])
                    self.push(htd(src[1:])-1)
            elif ct == 'POP':
                dest = self.f()
                if isreg(dest):
                    self.push(IS['pop'])
                    self.push(int(dest[1:])-1)
            elif ct == 'BRA':
                dest = self.f()
                if islabel(dest):
                    self.push(IS['bral'])
                    self.push(dest)
                elif isreg(dest):
                    self.push(IS['brar'])
                    self.push(htd(dest[1:])-1)
            elif ct == 'BRC':
                dest = self.f()
                if islabel(dest):
                    self.push(IS['brcl'])
                    self.push(dest)
                elif isreg(dest):
                    self.push(IS['brcr'])
                    self.push(htd(dest[1:])-1)
            elif ct == 'BNC':
                dest = self.f()
                if islabel(dest):
                    self.push(IS['bncl'])
                    self.push(dest)
                elif isreg(dest):
                    self.push(IS['bncr'])
                    self.push(htd(dest[1:])-1)
            elif ct == 'BRZ':
                dest = self.f()
                if islabel(dest):
                    self.push(IS['brzl'])
                    self.push(dest)
                elif isreg(dest):
                    self.push(IS['brzr'])
                    self.push(htd(dest[1:])-1)
            elif ct == 'BNZ':
                dest = self.f()
                if islabel(dest):
                    self.push(IS['bnzl'])
                    self.push(dest)
                elif isreg(dest):
                    self.push(IS['bnzr'])
                    self.push(htd(dest[1:])-1)
            elif ct == 'IMM':
                dest = self.f()
                src = self.f()
                if isreg(dest) and isnum(src):
                    self.push(IS['imm'])
                    self.push(htd(dest[1:])-1)
                    self.push((htd(src) >> 8) & 0xff)
                    self.push(htd(src) & 0xff)
                elif isreg(dest) and islabel(src):
                    self.push(IS['imm'])
                    self.push(htd(dest[1:])-1)
                    self.push(src)
                    
                    
            elif ct == 'MOV':
                src = self.f()
                dest = self.f()
                if isreg(src) and isreg(dest):
                    self.push(IS['mov'])
                    self.push(htd(dest[1:])-1)
                    self.push(htd(src[1:])-1)
                    
                    
            elif ct == 'ADD':
                dest = self.f()
                op1 = self.f()
                op2 = self.f()
                if isreg(dest):
                    if isnum(op1) and isnum(op2):
                        self.push(IS['addll'])
                        self.push(htd(dest[1:])-1)
                        self.push((htd(op1) >> 8) & 0xff)
                        self.push(htd(op1) & 0xff)
                        self.push((htd(op2) >> 8) & 0xff)
                        self.push(htd(op2) & 0xff)
                    elif isreg(op1) and isnum(op2):
                        self.push(IS['addrl'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(op1[1:])-1)
                        self.push((htd(op2) >> 8) & 0xff)
                        self.push(htd(op2) & 0xff)
                    elif isreg(op1) and isreg(op2):
                        self.push(IS['addrr'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(op1[1:])-1)
                        self.push(htd(op2[1:])-1)
            elif ct == 'AND':
                dest = self.f()
                op1 = self.f()
                op2 = self.f()
                if isreg(dest):
                    if isnum(op1) and isnum(op2):
                        self.push(IS['andll'])
                        self.push(htd(dest[1:])-1)
                        self.push((htd(op1) >> 8) & 0xff)
                        self.push(htd(op1) & 0xff)
                        self.push((htd(op2) >> 8) & 0xff)
                        self.push(htd(op2) & 0xff)
                    elif isreg(op1) and isnum(op2):
                        self.push(IS['andrl'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(op1[1:])-1)
                        self.push((htd(op2) >> 8) & 0xff)
                        self.push(htd(op2) & 0xff)
                    elif isreg(op1) and isreg(op2):
                        self.push(IS['andrr'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(op1[1:])-1)
                        self.push(htd(op2[1:])-1)
            elif ct == 'OR':
                dest = self.f()
                op1 = self.f()
                op2 = self.f()
                if isreg(dest):
                    if isnum(op1) and isnum(op2):
                        self.push(IS['orll'])
                        self.push(htd(dest[1:])-1)
                        self.push((htd(op1) >> 8) & 0xff)
                        self.push(htd(op1) & 0xff)
                        self.push((htd(op2) >> 8) & 0xff)
                        self.push(htd(op2) & 0xff)
                    elif isreg(op1) and isnum(op2):
                        self.push(IS['orrl'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(op1[1:])-1)
                        self.push((htd(op2) >> 8) & 0xff)
                        self.push(htd(op2) & 0xff)
                    elif isreg(op1) and isreg(op2):
                        self.push(IS['orrr'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(op1[1:])-1)
                        self.push(htd(op2[1:])-1)
            elif ct == 'XOR':
                dest = self.f()
                op1 = self.f()
                op2 = self.f()
                if isreg(dest):
                    if isnum(op1) and isnum(op2):
                        self.push(IS['xorll'])
                        self.push(htd(dest[1:])-1)
                        self.push((htd(op1) >> 8) & 0xff)
                        self.push(htd(op1) & 0xff)
                        self.push((htd(op2) >> 8) & 0xff)
                        self.push(htd(op2) & 0xff)
                    elif isreg(op1) and isnum(op2):
                        self.push(IS['xorrl'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(op1[1:])-1)
                        self.push((htd(op2) >> 8) & 0xff)
                        self.push(htd(op2) & 0xff)
                    elif isreg(op1) and isreg(op2):
                        self.push(IS['xorrr'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(op1[1:])-1)
                        self.push(htd(op2[1:])-1)
            elif ct == 'LOD':
                dest = self.f()
                src = self.f()
                if isreg(dest):
                    if isnum(src):
                        self.push(IS['lodl'])
                        self.push(htd(dest[1:])-1)
                        self.push((htd(src) >> 8) & 0xff)
                        self.push(htd(src) & 0xff)
                    elif isreg(src):
                        self.push(IS['lodr'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(src[1:])-1)
            elif ct == 'STORE':
                dest = self.f()
                src = self.f()
                if isnum(dest):
                    if isnum(src):
                        self.push(IS['strrml'])
                        self.push((htd(dest) >> 8) & 0xff)
                        self.push(htd(dest) &0xff)
                        self.push((htd(src) >> 8) & 0xff)
                        self.push(htd(src) & 0xff)
                    elif isreg(src):
                        self.push(IS['strrmr'])
                        self.push((htd(dest) >> 8) & 0xff)
                        self.push(htd(dest) &0xff)
                        self.push(htd(src[1:])-1)
                elif isreg(dest):
                    if isnum(src):
                        self.push(IS['strrl'])
                        self.push(htd(dest[1:])-1)
                        self.push((htd(src) >> 8) & 0xff)
                        self.push(htd(src) & 0xff)
                    elif isreg(src):
                        self.push(IS['strrr'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(src[1:])-1)
            elif ct == 'SUB':
                dest = self.f()
                op1 = self.f()
                op2 = self.f()
                #print(int(dest[1:])-1, op1, op2)
                if isreg(dest):
                    if isnum(op1) and isnum(op2):
                        self.push(IS['subll'])
                        self.push(htd(dest[1:])-1)
                        self.push((htd(op1) >> 8) & 0xff)
                        self.push(htd(op1) & 0xff)
                        self.push((htd(op2) >> 8) & 0xff)
                        self.push(htd(op2) & 0xff)
                    elif isreg(op1) and isnum(op2):
                        self.push(IS['subrl'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(op1[1:])-1)
                        self.push((htd(op2) >> 8) & 0xff)
                        self.push(htd(op2) & 0xff)
                    elif isnum(op1) and isreg(op2):
                        self.push(IS['sublr'])
                        self.push(htd(dest[1:])-1)
                        self.push((htd(op1) >> 8) & 0xff)
                        self.push(htd(op1) & 0xff)
                        self.push(htd(op2[1:])-1)
                    elif isreg(op1) and isreg(op2):
                        self.push(IS['subrr'])
                        self.push(htd(dest[1:])-1)
                        self.push(htd(op1[1:])-1)
                        self.push(htd(op2[1:])-1)
            elif ct == 'HLT':
                self.push(0xff)
            try:
                ct = self.f()
            except IndexError:
                print(self.labels)
                self.labels.update(_format_labels_(self.output))
                self.output[0] = self.bits
                self.output[1] = self.regs
                self.output[2] = ((self.ram >> 8) & 0xff)
                self.output[3] = self.ram & 0xff
                return self.pc(), self.labels, generateOffsetTable(self.labels)
                #return [0x0], {}, '@place 0'
            
I32 = {
    'cmpll': 0xf0,
    'cmprl': 0xf1,
    'cmplr': 0xf2,
    'cmprr': 0xf3,
    'jeql': 0xe0,
    'jeqr': 0xe1,
    'jnel': 0xe2,
    'jner': 0xe3,
    'jgl':  0xe4,
    'jgr': 0xe5,
    'jll': 0xe6,
    'jlr': 0xe7,
    'irql': 0xe8,
    'irqr': 0xe9,
}

class Compiler32:
    def __init__(self, code):
        self.code = code
        self.tokens = split(code)
        self.output = [0]*(2**16)
        self.cci = -1
        self.cti = 6
        self.labels = {}
        self.bits = 0
        self.ram = 0
        self.regs = 0
    def __clear_output__(self):
        while self.output[len(self.output)-1] == 0 and self.output[len(self.output)-2] == 0 and self.output[len(self.output)-3] == 0 and self.output[len(self.output)-4] == 0 and self.output[len(self.output)-5] == 0 and self.output[len(self.output)-6] == 0:
            nd = self.output[:-1]
            self.output = nd
        nd = []
        for i in range(len(self.output)):
            if type(self.output[i]) != str:
                nd.append(self.output[i])

        self.output = nd
    def f(self):
        self.cci += 1
        return self.tokens[self.cci]
    def fstr(self):
        start = self.f()
        string = ""
        if not start.startswith('"'): return
        else:
            string += start
            while not string.endswith('"'):
                start = self.f()
                string += ' '
                string += start
        return string
    def push(self, d):
        self.output[self.cti] = d
        self.cti += 1
    def pc(self):
        nd = []
        for dat in self.output:
            if type(dat) == str and islabel(dat):
                nd.append((self.labels[dat] >> 24) & 0xff if self.labels[dat] >= 0 else 0)
                nd.append((self.labels[dat] >> 16) & 0xff if self.labels[dat] >= 0 else 0)
                nd.append((self.labels[dat] >> 8) & 0xff if self.labels[dat] >= 0 else 0)
                nd.append(self.labels[dat] & 0xff if self.labels[dat] >= 0 else 0)
            elif isnum(str(dat)):
                nd.append(dat)
        self.output = nd
        return nd
    def c(self):
        ct = self.f()
        while ct != None:
            #print(ct)
            if ct == 'BITS':
                eqs = self.f()
                if eqs == '==' or eqs == '>=' or eqs == '<=':
                    self.bits = int(self.f())
            elif ct == 'MINREGS':
                eqs = self.f()
                if eqs == '==' or eqs == '>=' or eqs == '<=':
                    self.regs = int(self.f())
            elif ct == 'MINRAM':
                eqs = self.f()
                if eqs == '==' or eqs == '>=' or eqs == '<=':
                    self.ram = int(self.f())
            elif ct == '@org':
                offset = int(self.f())
                self.cti = offset
            elif ct == '@extern':
                label = self.f()
                offset = self.f()
                self.labels[label] = int(offset)
            elif ct == 'DB':
                d1 = self.f()
                if d1[0] == '"':
                    # string
                    self.cci -= 1
                    d1 = self.fstr()[1:-1]
                    for ch in d1:
                        self.push(ord(ch))
                else:
                    self.push(int(d1) & 0xff)
            elif ct == 'DW':
                d1 = self.f()
                self.push((int(d1) >> 8) & 0xff)
                self.push(int(d1) & 0xff)
            elif ct == 'DD':
                d1 = self.f()
                self.push((int(d1) >> 24) & 0xff)
                self.push((int(d1) >> 16)& 0xff)
                self.push((int(d1) >> 8) & 0xff)
                self.push(int(d1) & 0xff)
            elif ct.startswith('.'):
                self.push('r'+ct)
            elif ct == 'MOV':
                src = self.f()
                dest = self.f()
                self.push(IS['mov'])
                self.push(int(dest[1:])-1)
                self.push(int(src[1:])-1)
            elif ct == 'IMM':
                src = self.f()
                dest = self.f()
                self.push(IS['imm'])
                self.push(int(dest[1:])-1)
                self.push((int(src) >> 24) & 0xff)
                self.push((int(src) >> 16) & 0xff)
                self.push((int(src) >> 8) & 0xff)
                self.push((int(src)) & 0xff)
            elif ct == 'STORE':
                dest = self.f()
                typ = self.f()
                src = self.f()
                if isnum(src) and isnum(dest):
                    self.push(IS['strrml'])
                    self.push((int(dest) >> 24) & 0xff)
                    self.push((int(dest) >> 16) & 0xff)
                    self.push((int(dest) >> 8) & 0xff)
                    self.push(int(dest) & 0xff)
                    self.push(((int(src) >> 24) & 0xff) if typ == 'dword' else 0)
                    self.push(((int(src) >> 16) & 0xff) if typ == 'dword' else 0)
                    self.push(((int(src) >> 8) & 0xff) if typ == 'dword' or typ == 'word' else 0)
                    self.push(((int(src)) & 0xff) if typ == 'dword' or typ == 'word' or typ == 'byte' else 0)
                    self.push(4 if typ == 'dword' else 2 if typ == 'word' else 1 if typ == 'byte' else 0)
                elif isreg(src) and isnum(dest):
                    self.push(IS['strrmr'])
                    self.push((int(dest) >> 24) & 0xff)
                    self.push((int(dest) >> 16) & 0xff)
                    self.push((int(dest) >> 8) & 0xff)
                    self.push(int(dest) & 0xff)
                    self.push(int(src[1:])-1)
                    self.push(4 if typ == 'dword' else 2 if typ == 'word' else 1 if typ == 'byte' else 0)
                elif isreg(src) and isreg(dest):
                    self.push(IS['strrr'])
                    self.push(int(dest[1:])-1)
                    self.push(int(src[1:])-1)
                    self.push(4 if typ == 'dword' else 2 if typ == 'word' else 1 if typ == 'byte' else 0)
                elif isnum(src) and isreg(dest):
                    self.push(IS['strrl'])
                    self.push(int(dest[1:])-1)
                    self.push(((int(src) >> 24) & 0xff) if typ == 'dword' else 0)
                    self.push(((int(src) >> 16) & 0xff) if typ == 'dword' else 0)
                    self.push(((int(src) >> 8) & 0xff) if typ == 'dword' or typ == 'word' else 0)
                    self.push(((int(src)) & 0xff) if typ == 'dword' or typ == 'word' or typ == 'byte' else 0)
                    self.push(4 if typ == 'dword' else 2 if typ == 'word' else 1 if typ == 'byte' else 0)
            elif ct == 'LOD':
                dest = self.f()
                typ = self.f()
                src = self.f()
                if isreg(dest):
                    if isnum(src):
                        self.push(IS['lodl'])
                        self.push(int(dest[1:])-1)
                        self.push((int(src) >> 24) & 0xff)
                        self.push((int(src) >> 16) & 0xff)
                        self.push((int(src) >> 8) & 0xff)
                        self.push(int(src) & 0xff)
                        self.push(4 if typ == 'dword' else 2 if typ == 'word' else 1 if typ == 'byte' else 0)
                    elif isreg(src):
                        self.push(IS['lodl'])
                        self.push(int(dest[1:])-1)
                        self.push(int(src[1:])-1)
                        self.push(4 if typ == 'dword' else 2 if typ == 'word' else 1 if typ == 'byte' else 0)
            elif ct == 'HLT':
                self.push(0xff)
            elif ct == 'IRQ':
                data = self.f()
                if islabel(data):
                    self.push(I32['irql'])
                    self.push(data)
                elif isreg(data):
                    self.push(I32['irqr'])
                    self.push(int(data[1:])-1)
            elif ct == 'INT':
                inter = self.f()
                self.push(IS['int'])
                self.push(int(inter))
            elif ct == 'RET':
                self.push(IS['ret'])
            elif ct == 'PUSH':
                dat = self.f()
                if isnum(dat):
                    self.push(IS['pushl'])
                    self.push(int(dat))
                elif isreg(dat):
                    self.push(IS['pushr'])
                    self.push(int(dat[1:])-1)
            elif ct == 'POP':
                dest = self.f()
                if isreg(dest):
                    self.push(IS['pop'])
                    self.push(int(dest[1:])-1)
            elif ct == 'CMP':
                d1 = self.f()
                d2 = self.f()
                if isreg(d1) and isreg(d2):
                    self.push(I32['cmprr'])
                    self.push(int(d1[1:])-1)
                    self.push(int(d2[1:])-1)
                elif isreg(d1) and isnum(d2):
                    self.push(I32['cmprl'])
                    self.push(int(d1[1:])-1)
                    self.push((int(d2) >> 24) & 0xff)
                    self.push((int(d2) >> 16) & 0xff)
                    self.push((int(d2) >> 8) & 0xff)
                    self.push((int(d2)) & 0xff)
                elif isnum(d1) and isnum(d2):
                    self.push(I32['cmpll'])
                    self.push((int(d1) >> 24) & 0xff)
                    self.push((int(d1) >> 16) & 0xff)
                    self.push((int(d1) >> 8) & 0xff)
                    self.push((int(d1)) & 0xff)
                    self.push((int(d2) >> 24) & 0xff)
                    self.push((int(d2) >> 16) & 0xff)
                    self.push((int(d2) >> 8) & 0xff)
                    self.push((int(d2)) & 0xff)
            elif ct == 'JEQ':
                lbl = self.f()
                if islabel(lbl):
                    self.push(I32['jeql'])
                    self.push(lbl)
                elif isreg(lbl):
                    self.push(I32['jeqr'])
                    self.push(int(lbl[1:])-1)
            elif ct == 'JNE':
                lbl = self.f()
                if islabel(lbl):
                    self.push(I32['jnel'])
                    self.push(lbl)
                elif isreg(lbl):
                    self.push(I32['jner'])
                    self.push(int(lbl[1:])-1)
            elif ct == 'JMP':
                lbl = self.f()
                if islabel(lbl):
                    self.push(IS['bral'])
                    self.push(lbl)
                elif isreg(lbl):
                    self.push(IS['brar'])
                    self.push(int(lbl[1:])-1)
            elif ct == 'CAL':
                lbl = self.f()
                if islabel(lbl):
                    self.push(IS['call'])
                    self.push(lbl)
            elif ct == 'ADD':
                dest = self.f()
                op1 = self.f()
                op2 = self.f()
                if isreg(dest):
                    if isnum(op1) and isnum(op2):
                        self.push(IS['addll'])
                        self.push(int(dest[1:])-1)
                        self.push((int(op1) >> 24) & 0xff)
                        self.push((int(op1) >> 16) & 0xff)
                        self.push((int(op1) >> 8) & 0xff)
                        self.push((int(op1)) & 0xff)
                        self.push((int(op2) >> 24) & 0xff)
                        self.push((int(op2) >> 16) & 0xff)
                        self.push((int(op2) >> 8) & 0xff)
                        self.push((int(op2)) & 0xff)
                    elif isreg(op1) and isnum(op2):
                        self.push(IS['addrl'])
                        self.push(int(dest[1:])-1)
                        self.push(int(op1[1:])-1)
                        self.push((int(op2) >> 24) & 0xff)
                        self.push((int(op2) >> 16) & 0xff)
                        self.push((int(op2) >> 8) & 0xff)
                        self.push((int(op2)) & 0xff)
                    elif isreg(op1) and isreg(op2):
                        self.push(IS['addrr'])
                        self.push(int(op1[1:])-1)
                        self.push(int(op2[1:])-1)
            elif ct == 'SUB':
                dest = self.f()
                op1 = self.f()
                op2 = self.f()
                if isreg(dest):
                    if isnum(op1) and isnum(op2):
                        self.push(IS['subll'])
                        self.push(int(dest[1:])-1)
                        self.push((int(op1) >> 24) & 0xff)
                        self.push((int(op1) >> 16) & 0xff)
                        self.push((int(op1) >> 8) & 0xff)
                        self.push((int(op1)) & 0xff)
                        self.push((int(op2) >> 24) & 0xff)
                        self.push((int(op2) >> 16) & 0xff)
                        self.push((int(op2) >> 8) & 0xff)
                        self.push((int(op2)) & 0xff)
                    elif isreg(op1) and isnum(op2):
                        self.push(IS['subrl'])
                        self.push(int(dest[1:])-1)
                        self.push(int(op1[1:])-1)
                        self.push((int(op2) >> 24) & 0xff)
                        self.push((int(op2) >> 16) & 0xff)
                        self.push((int(op2) >> 8) & 0xff)
                        self.push((int(op2)) & 0xff)
                    elif isnum(op1) and isreg(op2):
                        self.push(IS['sublr'])
                        self.push(int(dest[1:])-1)
                        self.push((int(op1) >> 24) & 0xff)
                        self.push((int(op1) >> 16) & 0xff)
                        self.push((int(op1) >> 8) & 0xff)
                        self.push((int(op1)) & 0xff)
                        self.push(int(op2[1:])-1)
                    elif isreg(op1) and isreg(op2):
                        self.push(IS['sublr'])
                        self.push(int(dest[1:])-1)
                        self.push(int(op1[1:])-1)
                        self.push(int(op2[1:])-1)
            try: 
                #self.f()
                ct = self.f()
            except IndexError:
                #print('f')
                self.output[0] = self.bits
                self.output[1] = self.regs
                self.output[2] = (self.ram >> 24) & 0xff
                self.output[3] = (self.ram >> 16) & 0xff
                self.output[4] = (self.ram >> 8) & 0xff
                self.output[5] = (self.ram) & 0xff
               
                self.labels.update(_format_labels_(self.output))
                self.pc()
                self.__clear_output__()
                return self.output, self.labels


if sys.argv[3] == '8':
    co = Compiler8(open(sys.argv[1], 'r').read())
    d, labs = co.c()
    #print(d, labs)
    open(sys.argv[2], 'wb').write(bytearray(d))
elif sys.argv[3] == '16':
    co = Compiler16(open(sys.argv[1], 'r').read())
    d, labs, oft = co.c()
    boft = []
    for d_ in oft:
        boft.append(ord(d_))
    #print(labs)
    open(sys.argv[2], 'wb').write(bytearray(boft+d))
    #open(sys.argv[4], 'w').write(oft)
elif sys.argv[3] == '32':
    co = Compiler32(open(sys.argv[1], 'r').read())
    d, labs = co.c()
    print(d, labs)
    open(sys.argv[2], 'wb').write(bytearray(d))

#print(split(open(sys.argv[1], 'r').read()))