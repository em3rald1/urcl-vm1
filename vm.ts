/*
    URCL VM:
        virtual machine based on cpu built in minecraft
*/

type int = number;

import { readLines } from "https://deno.land/std@0.76.0/io/bufio.ts";

async function promptString() {
    //console.log(question);

    for await (const line of readLines(Deno.stdin)) {
        return line;
    }
}

const IS = {
    'addrr': 1, // a + b
    'addrl': 2, //  a + 5
    'addll': 3, // add 5 + 45
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
    'int': 0xfd,
};

export class URCL8
{
    registers : Uint8Array;
    memory : Uint8Array;
    ip: int;
    cf: boolean = false;
    zf: boolean = true;
    constructor(bitness : int, minregs : int, minram : int, stackneeded: boolean = false) 
    {
        if(bitness > 8) {
            throw new TypeError(`This VM isn't supporting more than 8 bits!`)
        }
        if(stackneeded) {
            throw new TypeError(`This VM isn't supporting stack!`);
        }
        this.registers = new Uint8Array(minregs);
        this.memory = new Uint8Array(minram);
        this.ip = 0
    };
    fetch() : int {
        //this.ip += 1;
        return this.memory[this.ip++];
    }
    execute() : boolean {
        let result = false;
        let instruction : int = this.fetch();
       // console.log(this.ip)
        switch(instruction) {
            case IS.addrr: {
                let dest = this.fetch();
                let r1 = this.fetch();
                let r2 = this.fetch();
                this.registers[dest] = this.registers[r1] + this.registers[r2];
                this.cf = this.registers[r1] + this.registers[r2] > 255;
                this.zf = this.registers[r1] + this.registers[r2] == 0;
                console.log(`[Exec] [Instruction: ${instruction}(ADD), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.addrl: {
                let dest = this.fetch();
                let r1 = this.fetch();
                let l1 = this.fetch();
                this.registers[dest] = this.registers[r1] + l1;
                this.cf = this.registers[r1] + l1 > 255;
                this.zf = this.registers[r1] + l1 == 0;
                console.log(`[Exec] [Instruction: ${instruction}(ADD), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            
            case IS.addll: {
                let dest = this.fetch();
                let l1 = this.fetch();
                let l2 = this.fetch();
                this.registers[dest] = l1 + l2;
                this.cf = l1 + l2 > 255;
                this.zf = l1 + l2 == 0;
                console.log(`[Exec] [Instruction: ${instruction}(ADD), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.subrr: {
                let dest = this.fetch();
                let r1 = this.fetch();
                let r2 = this.fetch();
                this.registers[dest] = this.registers[r1] - this.registers[r2];
                this.cf = this.registers[r1] - this.registers[r2] > 255;
                this.zf = this.registers[r1] - this.registers[r2] == 0;
                console.log(`[Exec] [Instruction: ${instruction}(SUB), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.subrl: {
                let dest = this.fetch();
                let r1 = this.fetch();
                let l1 = this.fetch();
                this.registers[dest] = this.registers[r1] - l1;
                this.cf = this.registers[r1] - l1 > 255;
                this.zf = this.registers[r1] - l1 == 0;
                console.log(`[Exec] [Instruction: ${instruction}(SUB), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.sublr: {
                let dest = this.fetch();
                let l1 = this.fetch();
                let r1 = this.fetch();
                this.registers[dest] = l1 - this.registers[r1];
                this.cf = l1 - this.registers[r1] > 255;
                this.zf = l1 - this.registers[r1] == 0;
                console.log(`[Exec] [Instruction: ${instruction}(SUB), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.subll: {
                let dest = this.fetch();
                let l1 = this.fetch();
                let l2 = this.fetch();
                this.registers[dest] = l1 - l2;
                this.cf = l1 - l2 > 255;
                this.zf = l1 - l2 == 0;
                console.log(`[Exec] [Instruction: ${instruction}(SUB), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.rshl: {
                let dest = this.fetch();
                let l1 = this.fetch();
                this.registers[dest] = l1 >> 1;
                console.log(`[Exec] [Instruction: ${instruction}(RSH), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.rshr: {
                let dest = this.fetch();
                let r1 = this.fetch();
                this.registers[dest] = this.registers[r1] >> 1;
                console.log(`[Exec] [Instruction: ${instruction}(RSH), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.lshl: {
                let dest = this.fetch();
                let l1 = this.fetch();
                this.registers[dest] = l1 << 1;
                console.log(`[Exec] [Instruction: ${instruction}(LSH), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.lshr: {
                let dest = this.fetch();
                let r1 = this.fetch();
                this.registers[dest] = this.registers[r1] << 1;
                console.log(`[Exec] [Instruction: ${instruction}(LSH), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.incl: {
                let dest = this.fetch();
                let l1 = this.fetch();
                this.registers[dest] = l1 + 1;
                this.cf = l1 + 1 > 255;
                this.zf = l1 + 1 == 0;
                console.log(`[Exec] [Instruction: ${instruction}(INC), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.incr: {
                let dest = this.fetch();
                let r1 = this.fetch();
                this.registers[dest] = this.registers[r1] + 1;
                this.cf = this.registers[r1] + 1 > 255;
                this.zf = this.registers[r1] + 1 == 0;
                console.log(`[Exec] [Instruction: ${instruction}(INC), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.decl: {
                let dest = this.fetch();
                let l1 = this.fetch();
                this.registers[dest] = l1-1;
                this.cf = l1-1 > 255;
                this.zf = l1-1 == 0;
                console.log(`[Exec] [Instruction: ${instruction}(DEC), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.decr: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                this.registers[dest] = r1-1;
                this.cf = r1-1 > 255;
                this.zf = r1-1 == 0;
                console.log(`[Exec] [Instruction: ${instruction}(DEC), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.xorrr: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let r2 = this.registers[this.fetch()];
                this.registers[dest] = r1 ^ r2;
                this.cf = (r1 ^ r2) > 255;
                this.zf = (r1 ^ r2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(XOR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.xorrl: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let l1 = this.fetch();
                this.registers[dest] = r1 ^ l1;
                this.cf = (r1 ^ l1) > 255;
                this.zf = (r1 ^ l1) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(XOR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.xorll: {
                let dest = this.fetch();
                let l1 = this.fetch();
                let l2 = this.fetch();
                this.registers[dest] = l1 ^ l2;
                this.cf = (l1 ^ l2) > 255;
                this.zf = (l1 ^ l2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(XOR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.andll: {
                let dest = this.fetch();
                let l1 = this.fetch();
                let l2 = this.fetch();
                this.registers[dest] = l1 & l2;
                this.cf = (l1 & l2) > 255;
                this.zf = (l1 & l2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(AND), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.andrl: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let l1 = this.fetch();
                this.registers[dest] = r1 & l1;
                this.cf = (l1 & r1) > 255;
                this.zf = (l1 & r1) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(AND), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.andrr: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let r2 = this.registers[this.fetch()];
                this.registers[dest] = r1 & r2;
                this.cf = (r1 & r2) > 255;
                this.zf = (r1 & r2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(AND), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.orll: {
                let dest = this.fetch();
                let l1 = this.fetch();
                let l2 = this.fetch();
                this.registers[dest] = l1 | l2;
                this.cf = (l1 | l2) > 255;
                this.zf = (l1 | l2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(OR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.orrl: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let l1 = this.fetch();
                this.registers[dest] = r1 | l1;
                this.cf = (l1 | r1) > 255;
                this.zf = (l1 | r1) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(OR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.orrr: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let r2 = this.registers[this.fetch()];
                this.registers[dest] = r1 | r2;
                this.cf = (r1 | r2) > 255;
                this.zf = (r1 | r2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(OR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.nandll: {
                let dest = this.fetch();
                let l1 = this.fetch();
                let l2 = this.fetch();
                this.registers[dest] = ~(l1 & l2);
                this.cf = ~(l1 & l2) > 255;
                this.zf = ~(l1 & l2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(NAND), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.nandrl: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let l1 = this.fetch();
                this.registers[dest] = ~(r1 & l1);
                this.cf = ~(l1 & r1) > 255;
                this.zf = ~(l1 & r1) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(NAND), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.nandrr: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let r2 = this.registers[this.fetch()];
                this.registers[dest] = ~(r1 & r2);
                this.cf = ~(r1 & r2) > 255;
                this.zf = ~(r1 & r2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(NAND), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.norll: {
                let dest = this.fetch();
                let l1 = this.fetch();
                let l2 = this.fetch();
                this.registers[dest] = ~(l1 | l2);
                this.cf = ~(l1 | l2) > 255;
                this.zf = ~(l1 | l2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(NOR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.norrl: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let l1 = this.fetch();
                this.registers[dest] = ~(r1 | l1);
                this.cf = ~(l1 | r1) > 255;
                this.zf = ~(l1 | r1) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(NOR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.norrr: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let r2 = this.registers[this.fetch()];
                this.registers[dest] = ~(r1 | r2);
                this.cf = ~(r1 | r2) > 255;
                this.zf = ~(r1 | r2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(NOR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.xnorll: {
                let dest = this.fetch();
                let l1 = this.fetch();
                let l2 = this.fetch();
                this.registers[dest] = ~(l1 ^ l2);
                this.cf = ~(l1 ^ l2) > 255;
                this.zf = ~(l1 ^ l2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(XNOR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.xnorrl: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let l1 = this.fetch();
                this.registers[dest] = ~(r1 & l1);
                this.cf = ~(l1 ^ r1) > 255;
                this.zf = ~(l1 ^ r1) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(XNOR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.xnorrr: {
                let dest = this.fetch();
                let r1 = this.registers[this.fetch()];
                let r2 = this.registers[this.fetch()];
                this.registers[dest] = ~(r1 & r2);
                this.cf = ~(r1 ^ r2) > 255;
                this.zf = ~(r1 ^ r2) == 0;
                console.log(`[Exec] [Instruction: ${instruction}(XNOR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.notl: {
                let dest = this.fetch();
                let l1 = this.fetch();
                this.registers[dest]= ~l1;
                this.cf = ~l1 > 255;
                this.zf = ~l1 == 0;
                console.log(`[Exec] [Instruction: ${instruction}(NOT), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.notr: {
                let dest = this.fetch();
                let r1 = this.fetch();
                this.registers[dest] = ~this.registers[r1];
                this.cf = ~this.registers[r1] > 255;
                this.zf = ~this.registers[r1] == 0;
                console.log(`[Exec] [Instruction: ${instruction}(NOT), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.mov: {
                let src = this.fetch();
                let dest = this.fetch();
                this.registers[dest] = this.registers[src];
                console.log(`[Exec] [Instruction: ${instruction}(MOV), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.imm: {
                let src = this.fetch();
                let dest = this.fetch();
                this.registers[dest] = src;
                console.log(`[Exec] [Instruction: ${instruction}(IMM), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.lodl: {
                let dest = this.fetch();
                let addr = this.fetch();
                this.registers[dest] = this.memory[addr];
                console.log(`[Exec] [Instruction: ${instruction}(LOD), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.lodr: {
                let dest = this.fetch();
                let r1 = this.fetch();
                this.registers[dest] = this.memory[this.registers[r1]];
                console.log(`[Exec] [Instruction: ${instruction}(LOD), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.strrmr: {
                let src = this.fetch();
                let addr = this.fetch();
                this.memory[addr] = this.registers[src];
                console.log(`[Exec] [Instruction: ${instruction}(STR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.strrr: {
                let src = this.fetch();
                let addr = this.registers[this.fetch()];
                this.memory[addr] = this.registers[src];
                console.log(`[Exec] [Instruction: ${instruction}(STR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.strrml: {
                let src = this.fetch();
                let addr = this.fetch();
                this.memory[addr] = src;
                console.log(`[Exec] [Instruction: ${instruction}(STR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.strrl: {
                let src = this.fetch();
                let addr = this.registers[this.fetch()];
                console.log(`[Exec] [Instruction: ${instruction}(STR), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                this.memory[addr] = src;
                break;
            }
            case IS.brarl: {
                let reladdr = this.fetch();
                this.ip += reladdr;
                console.log(`[Exec] [Instruction: ${instruction}(BRA), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.bral: {
                let addr = this.fetch();
                this.ip = addr;
                console.log(`[Exec] [Instruction: ${instruction}(BRA), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.brar: {
                let addr = this.registers[this.fetch()];
                this.ip = addr;
                console.log(`[Exec] [Instruction: ${instruction}(BRA), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            }
            case IS.brcrl: {
                let reladdr = this.fetch();
                if (this.cf) {
                    this.ip += reladdr;
                    console.log(`[Exec] [Instruction: ${instruction}(BRС), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                }
                break;
            }
            case IS.brcl: {
                let addr = this.fetch();
                if ( this.cf ) {
                    this.ip = addr;
                    console.log(`[Exec] [Instruction: ${instruction}(BRС), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                }
                break;
            }
            case IS.brcr: {
                let addr = this.registers[this.fetch()];
                if(this.cf) {
                    this.ip = addr;
                    console.log(`[Exec] [Instruction: ${instruction}(BRС), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                }
                break;
            }
            case IS.bncrl: {
                let reladdr = this.fetch();
                if (!this.cf) {
                    this.ip += reladdr;
                    console.log(`[Exec] [Instruction: ${instruction}(BNС), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                }
                break;
            }
            case IS.bncl: {
                let addr = this.fetch();
                if (! this.cf ) {
                    this.ip = addr;
                    console.log(`[Exec] [Instruction: ${instruction}(BNС), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                }
                break;
            }
            case IS.bncr: {
                let addr = this.registers[this.fetch()];
                if(!this.cf) {
                    this.ip = addr;
                    console.log(`[Exec] [Instruction: ${instruction}(BNС), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                }
                break;
            }
            case IS.brzrl: {
                let reladdr = this.fetch();
                if (this.zf) {
                    this.ip += reladdr;
                    console.log(`[Exec] [Instruction: ${instruction}(BRZ), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                }
                break;
            }
            case IS.brzl: {
                let addr = this.fetch();
                if ( this.zf ) {
                    this.ip = addr;
                    console.log(`[Exec] [Instruction: ${instruction}(BRZ), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                }
                break;
            }
            case IS.brzr: {
                let addr = this.registers[this.fetch()];
                if(this.zf) {
                    this.ip = addr;
                    console.log(`[Exec] [Instruction: ${instruction}(BRZ), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                }
                break;
            }
            case IS.nop: {
                console.log(`[Exec] [Instruction: ${instruction}(NOP), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                break;
            };
            case IS.hlt: {
                console.log(`[Exec] [Instruction: ${instruction}(HLT), Zero Flag: ${this.zf ? 1 : 0}, Carry Flag ${this.cf ? 1 : 0}]`)
                result = true;
                break;
            }
            default:
                console.log(`[Exec] [Illegal operator ${instruction}!]`)
                result = true;
        }
        console.log(`[MEMORY NEAR IP: [ ${this.memory.slice(this.ip-2, this.ip+5)} ] ]`)
        console.log(`[IP: ${this.ip}]`)
        return result;
    }
    load(data : Uint8Array, offset: int = 0) : void {
        for(let o : int = 0; o < data.length; o++) {
            this.memory[o+offset] = data[o];
        }
    }
    start(ip: int = 0) {
        this.ip = ip;
        let i = false;
        while (!i) {
            i = this.execute();
            console.log(`[ REGISTER DATA: [ ${this.registers} ] ]`)
            if(i) break;
        }
    }
};



export class URCL16
{
    memory: Uint8Array;
    regs: Uint16Array;
    ip : int;
    sp : int;
    zf: boolean = true; 
    cf : boolean = false;
    storedAddress: int = 0;
    constructor(bitness: number, regs: number, ram: number) {
        if(bitness > 16) throw new TypeError('This VM isn\'t supporting more than 16 bits!');
        this.regs = new Uint16Array(regs);
        this.memory = new Uint8Array(ram);
        this.ip = -1;
        this.sp = ram;
    }
    push(d : int): void {
        this.memory[this.sp] = d;
        this.sp--;
    }
    pop() : int {
        this.sp++;
        return this.memory[this.sp];
    }
    fetch() : int {
        return this.memory[this.ip++];
    }
    fetch16() : int {
        let d1 = this.fetch();
        let d2 = this.fetch();
        //console.log((d1  << 8) | d2);
        //this.fetch();
        return (d1 << 8) | d2;
    }
    execute() : boolean {
        let res = false;
        let instruction = this.fetch();
        switch(instruction) {
            case IS.out: {
                let src = this.fetch16();
                Deno.stdout.write(new Uint8Array([this.memory[src]]));
                break;
            }
            case IS.andll: {
                let dest = this.fetch();
                let op1  = this.fetch16();
                let op2  = this.fetch16();
                this.regs[dest] = op1 & op2;
                this.zf = (op1 & op2) == 0;
                this.cf = (op1 & op2) > 2*16;
                break;
            }
            case IS.andrl: {
                let dest = this.fetch();
                let op1  = this.regs[this.fetch()];
                let op2  = this.fetch16();
                this.regs[dest] = op1 & op2;
                this.zf = (op1 & op2) == 0;
                this.cf = (op1 & op2) > 2*16;
                break;
            }
            case IS.int: {
                // interrupt
                let int_ = this.fetch();
                switch(int_) {
                    case 10: { // stdout::write
                        Deno.stdout.writeSync(this.memory.slice(400, 416));
                        //console.log(this.memory.slice(400, 416))
                        break;
                    } 
                }
                break;
            }
            case IS.andrr: {
                let dest = this.fetch();
                let op1  = this.regs[this.fetch()];
                let op2  = this.regs[this.fetch()];
                this.regs[dest] = op1 & op2;
                this.zf = (op1 & op2) == 0;
                this.cf = (op1 & op2) > 2*16;
                break;
            }
            case IS.orll: {
                let dest = this.fetch();
                let op1  = this.fetch16();
                let op2  = this.fetch16();
                this.regs[dest] = op1 | op2;
                this.zf = (op1 | op2) == 0;
                this.cf = (op1 | op2) > 2*16;
                break;
            }
            case IS.orrl: {
                let dest = this.fetch();
                let op1  = this.regs[this.fetch()];
                let op2  = this.fetch16();
                this.regs[dest] = op1 | op2;
                this.zf = (op1 | op2) == 0;
                this.cf = (op1 | op2) > 2*16;
                break;
            }
            case IS.orrr: {
                let dest = this.fetch();
                let op1  = this.regs[this.fetch()];
                let op2  = this.regs[this.fetch()];
                this.regs[dest] = op1 | op2;
                this.zf = (op1 | op2) == 0;
                this.cf = (op1 | op2) > 2*16;
                break;
            }
            case IS.xorll: {
                let dest = this.fetch();
                let op1  = this.fetch16();
                let op2  = this.fetch16();
                this.regs[dest] = op1 ^ op2;
                this.zf = (op1 ^ op2) == 0;
                this.cf = (op1 ^ op2) > 2*16;
                break;
            }
            case IS.xorrl: {
                let dest = this.fetch();
                let op1  = this.regs[this.fetch()];
                let op2  = this.fetch16();
                this.regs[dest] = op1 ^ op2;
                this.zf = (op1 ^ op2) == 0;
                this.cf = (op1 ^ op2) > 2*16;
                break;
            }
            case IS.xorrr: {
                let dest = this.fetch();
                let op1  = this.regs[this.fetch()];
                let op2  = this.regs[this.fetch()];
                this.regs[dest] = op1 | op2;
                this.zf = (op1 ^ op2) == 0;
                this.cf = (op1 ^ op2) > 2*16;
                break;
            }
            case IS.notl: {
                let dest = this.fetch();
                let op1 = this.fetch16();
                this.regs[dest] = ~op1;
                this.zf = ~op1 == 0;
                break;
            }
            case IS.pushl: {
                let src = this.fetch16();
                this.push((src >> 8) & 0xff);
                this.push(src & 0xff);
                break;
            }
            case IS.pushr: {
                let src = this.regs[this.fetch()];
                this.push((src >> 8) & 0xff);
                this.push(src & 0xff);
                break;
            }
            case IS.pop: {
                let dest = this.fetch();
                let d1 = this.pop();
                let d2 = this.pop();
                this.regs[dest] = (d2 << 8) | d1;
                break;
            }
            case IS.notr:{ 
                let dest = this.fetch();
                let op1  = this.regs[this.fetch()];
                this.regs[dest] = ~op1;
                this.zf = ~op1 == 0;
                break;
            }
            case IS.addll: {
                let dest = this.fetch();
                let op1 = this.fetch16();
                let op2 = this.fetch16();
                this.regs[dest] = op1 + op2;
                this.zf = op1 + op2 == 0;
                this.cf = op1 + op2 > 2**16;
                break;
            }
            case IS.addrl: {
                let dest = this.fetch();
                let op1 = this.regs[this.fetch()];
                let op2 = this.fetch16();
                this.regs[dest] = op1 + op2;
                this.zf = op1 + op2 == 0;
                this.cf = op1 + op2 > 2**16;
                break;
            }
            case IS.addrr: {
                let dest = this.fetch();
                let op1 = this.regs[this.fetch()];
                let op2 = this.regs[this.fetch()];
                this.regs[dest] = op1 + op2;
                this.zf = op1 + op2 == 0;
                this.cf = op1 + op2 > 2**16;
                break;
            }
            case IS.subll:{
                let dest = this.fetch();
                let op1 = this.fetch16();
                let op2 = this.fetch16();
                this.regs[dest] = op1 - op2;
                this.zf = op1 - op2 == 0;
                this.cf = op1 - op2 > 2**16;
                break;
            }
            case IS.sublr: {
                let dest = this.fetch();
                let op1 = this.fetch16();
                let op2 = this.regs[this.fetch()];
                this.regs[dest] = op1 - op2;
                this.zf = op1 - op2 == 0;
                this.cf = op1 - op2 > 2**16;
                break;
            }
            case IS.subrl: {
                let dest = this.fetch();
                let op1 = this.regs[this.fetch()];
                let op2 = this.fetch16();
                this.regs[dest] = op1 - op2;
                this.zf = op1 - op2 == 0;
                this.cf = op1 - op2 > 2**16;
                break;
            }
            case IS.subrr: {
                let dest = this.fetch();
                let op1 = this.regs[this.fetch()];
                let op2 = this.regs[this.fetch()];
                this.regs[dest] = op1 - op2;
                //console.log('[DBG]',dest, op1, op2)
                this.zf = op1 - op2 == 0;
                this.cf = op1 - op2 > 2**16;
                break;
            }
            case IS.rshl: {
                let dest = this.fetch();
                let l1 = this.fetch16();
                this.regs[dest] = l1 >> 1;
                this.zf = l1 >> 1 == 0;
                this.cf = l1 >> 1 > 2**16;
                break;
            }
            case IS.rshr: {
                let dest = this.fetch();
                let l1 = this.regs[this.fetch()];
                this.regs[dest] = l1 >> 1;
                this.zf = l1 >> 1 == 0;
                this.cf = l1 >> 1 > 2**16;
                break;
            }
            case IS.lshl: {
                let dest = this.fetch();
                let l1 = this.fetch16();
                this.regs[dest] = l1 << 1;
                this.zf = l1 << 1 == 0;
                this.cf = l1 << 1 > 2**16;
                break;
            }
            case IS.lshr: {
                let dest = this.fetch();
                let l1 = this.regs[this.fetch()];
                this.regs[dest] = l1 << 1;
                this.zf = l1 << 1 == 0;
                this.cf = l1 << 1 > 2**16;
                break;
            }
            case IS.incr: {
                let dest = this.fetch();
                let l1 = this.regs[this.fetch()];
                this.regs[dest] = l1 + 1;
                this.zf = l1 + 1 == 0;
                this.cf = l1 + 1 > 2**16;
                break;
            }
            case IS.incl: {
                let dest = this.fetch();
                let l1 = this.fetch16();
                this.regs[dest] = l1 + 1;
                this.zf = l1 + 1 == 0;
                this.cf = l1 + 1 > 2**16;
                break;
            }
            case IS.decl: {
                let dest = this.fetch();
                let l1 = this.fetch16();
                this.regs[dest] = l1 - 1;
                this.zf = l1 - 1 == 0;
                this.cf = l1 - 1 > 2**16;
                break;
            }
            case IS.decr: {
                let dest = this.fetch();
                let l1 = this.regs[this.fetch()];
                this.regs[dest] = l1 - 1;
                this.zf = l1 - 1 == 0;
                this.cf = l1 - 1 > 2**16;
                break;
            }
            case IS.imm: {
                let dest = this.fetch();
                let src = this.fetch16();
                this.regs[dest] = src;
                break;
            }
            case IS.call: {
                let dest = this.fetch16();
                this.push(this.ip >> 8);
                this.push(this.ip);
                this.ip = dest;
                break;
            }
            case IS.calr: {
                let dest = this.regs[this.fetch()];
                this.push(this.ip >> 8);
                this.push(this.ip);
                this.ip = dest;
                break;
            }
            case IS.ret: {
                let d1 = this.pop();
                let d2 = this.pop();
                this.ip = (d2 << 8) | d1;
                break;
            }
            case IS.brarl: {
                let dest = this.fetch16();
                this.ip += dest;
                break;
            }
            case IS.brar: {
                let dest = this.regs[this.fetch()];
                this.ip = dest;
                break;
            }
            case IS.bral: {
                let dest = this.fetch16();
                this.ip = dest;
                break;
            }
            case IS.brcrl: {
                let dest = this.fetch16();
                if(this.cf)
                    this.ip += dest;
                break;
            }
            case IS.brcr: {
                let dest = this.regs[this.fetch()];
                if(this.cf)
                this.ip = dest;
                break;
            }
            case IS.brcl: {
                let dest = this.fetch16();
                if(this.cf)
                this.ip = dest;
                break;
            }
            case IS.bncrl: {
                let dest = this.fetch16();
                if(!this.cf)
                this.ip += dest;
                break;
            }
            case IS.bncr: {
                let dest = this.regs[this.fetch()];
                if(!this.cf)
                this.ip = dest;
                break;
            }
            case IS.bncl: {
                let dest = this.fetch16();
                if(!this.cf)
                this.ip = dest;
                break;
            }
            case IS.brzrl: {
                let dest = this.fetch16();
                if(this.zf)
                this.ip += dest;
                break;
            }
            case IS.brzr: {
                let dest = this.regs[this.fetch()];
                if(this.zf)
                this.ip = dest;
                break;
            }
            case IS.brzl: {
                let dest = this.fetch16();
                if(this.zf)
                this.ip = dest;
                break;
            }
           // debugger;
            case IS.bnzrl: {
                let dest = this.fetch16();
                if(!this.zf)
                this.ip += dest;
                break;
            }
            case IS.bnzr: {
                let dest = this.regs[this.fetch()];
                if(!this.zf)
                this.ip = dest;
                break;
            }
            case IS.bnzl: {
                let dest = this.fetch16();
                if(!this.zf)
                this.ip = dest;
                break;
            }
            case IS.mov: {
                let dest = this.fetch();
                let src = this.regs[this.fetch()];
                this.regs[dest] = src;
                break;
            }
            case IS.lodl: {
                let dest = this.fetch();
                let src = this.fetch16();
                this.regs[dest] = (this.memory[src] << 8) | this.memory[src+1];
                break;
            }
            case IS.lodr: {
                let dest = this.fetch();
                let src = this.regs[this.fetch()];
                this.regs[dest] = (this.memory[src] << 8) | this.memory[src+1];
                break;
            }
            case IS.strrml: {
                let dest = this.fetch16();
                let src = this.fetch16();
                this.memory[dest+1] = src & 0xff;
                this.memory[dest] = (src >> 8) & 0xff;
                break;
            }
            case IS.strrmr: {
                let dest = this.fetch16();
                let src = this.regs[this.fetch()];
                this.memory[dest+1] = src & 0xff;
                this.memory[dest] = (src >> 8) & 0xff;
                break;
            }
            case IS.strrl: {
                let dest = this.regs[this.fetch()];
                let src = this.fetch16();
                this.memory[dest+1] = src & 0xff;
                this.memory[dest] = (src >> 8) & 0xff;
                break;
            }
            case IS.strrr: {
                let dest = this.regs[this.fetch()];
                let src = this.regs[this.fetch()];
                this.memory[dest+1] = src & 0xff;
                this.memory[dest] = (src >> 8) & 0xff;
                break;
            }
            case IS.hlt: {
                res = true;
                break;
            }
            default: {
                res = true;
                break;
            }
        }
        //console.log(`EIP: ${this.ip}`)
        //console.log(`INSTRUCTION: ${instruction}`)
        return res;
    }
    load(data: Uint8Array, off: int = 0) {
        for(let i = 0; i < data.length; i++) {
            this.memory[i+off] = data[i];
            //data[i] ? console.log(`Loaded symbol: ${data[i]}`) : null;
        }
    }
    start(ip: int = this.ip) {
        this.ip = ip >= 0 ? ip : 0;
        let i = false;
        while (!i) {
            i = this.execute();
            //console.log(`[ REGISTER DATA: [ ${this.regs} ] ]`)
            if(i) break;
        }
        //console.log(`[PROGRAM TERMINATED WITH CODE ${this.regs[0]}]`)
    }
};