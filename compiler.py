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
    'out': 0xfe
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
                labels[ct[1:]] = i-3
    return labels

def generateOffsetTable(labels = {}):
    data = ""
    for label in labels:
        data += f"{label}: @org {labels[label]}\n"
    return data

def htd(d=''):
    if d.startswith('0x'):
        return int(d[2:], 16)
    elif d.endswith('h'):
        return int(d[:-1], 16)
    elif isnum(d):
        return int(d)

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
    def include(self, binary='', filee=""):
        self.INCLUDE_OFFSET = 0
        data = open(filee, 'r').read()
        lines = data.splitlines()
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
        bdata = open(binary, 'rb').read()
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
                oftFile = self.f()
                if binFile.startswith("\"") and binFile.endswith('"') and oftFile.startswith("\"") and oftFile.endswith('"'):
                    self.include(binFile[1:-1], oftFile[1:-1])
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

if sys.argv[3] == '8':
    co = Compiler8(open(sys.argv[1], 'r').read())
    d, labs = co.c()
    #print(d, labs)
    open(sys.argv[2], 'wb').write(bytearray(d))
elif sys.argv[3] == '16':
    co = Compiler16(open(sys.argv[1], 'r').read())
    d, labs, oft = co.c()
    #print(labs)
    open(sys.argv[2], 'wb').write(bytearray(d))
    open(sys.argv[4], 'w').write(oft)


#print(split(open(sys.argv[1], 'r').read()))