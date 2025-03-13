import sys
from MemoriaCache import MemoriaCache
import os

cwd = os.getcwd()

CPU_DEBUG = True

OPCODES = {
    "cp": 0x01,
    "ax": 0x02,
    "bx": 0x03,
    "cx": 0x04,
    "dx": 0x05,
    "add_reg_byte": 0x00,
    "add_reg_reg": 0x01,
    "inc": 0x10,
    "dec": 0x20,
    "sub_reg_byte": 0x30,
    "sub_reg_reg": 0x31,
    "mov_reg_byte": 0x40,
    "mov_reg_reg": 0x41,
    "jmp": 0x50,
    "cmp_reg_byte": 0x60,
    "cmp_reg_reg": 0x61,
    "jz": 0x70,
    "jz_bug": 79,

}

registrador_cp = 0x00
registrador_ax = 0x00
registrador_bx = 0x00
registrador_cx = 0x00
registrador_dx = 0x00

flag_zero = False


#memoria = MemoriaCache('arquivos_memoria/mov_mov_add.bin')
#memoria = MemoriaCache('arquivos_memoria/inc_dec.bin')
#memoria = MemoriaCache('arquivos_memoria/todas_instrucoes.bin')
#memoria = MemoriaCache('arquivos_memoria/programa_simples.bin')
memoria = MemoriaCache('arquivos_memoria/fibonacci_10.bin')

def buscarEDecodificarInstrucao():
    global registrador_ax
    global registrador_bx
    global registrador_cp
    global registrador_cx
    global registrador_dx
    global flag_zero

    instrucao = memoria.getValorMemoria(registrador_cp)

    if instrucao in OPCODES.values():
        return instrucao

    return -1

def getRegistrador(reg_opcode):
    global registrador_ax
    global registrador_bx
    global registrador_cp
    global registrador_cx
    global registrador_dx
    global flag_zero

    if reg_opcode == OPCODES["ax"]:
        return registrador_ax

    elif reg_opcode == OPCODES["bx"]:
        return registrador_bx

    elif reg_opcode == OPCODES["cx"]:
        return registrador_cx
    
    elif reg_opcode == OPCODES["dx"]:
        return registrador_dx

    else:
        print("Erro ao pegar registrador")
        return 0

def setRegistrador(reg_opcode, valor):
    global registrador_ax
    global registrador_bx
    global registrador_cp
    global registrador_cx
    global registrador_dx
    global flag_zero

    if reg_opcode == OPCODES["cp"]:
        registrador_cp = valor

    elif reg_opcode == OPCODES["ax"]:
        registrador_ax = valor

    elif reg_opcode == OPCODES["bx"]:
        registrador_bx = valor

    elif reg_opcode == OPCODES["cx"]:
        registrador_cx = valor
    
    elif reg_opcode == OPCODES["dx"]:
        registrador_dx = valor

    else:
        print("Erro ao setar registrador")


def lerOperadoresExecutarInstrucao(idInstrucao):
    global flag_zero
    global registrador_cp

    # Verifica instrucao
    if idInstrucao == OPCODES['add_reg_byte']:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)
        operador2 = memoria.getValorMemoria(registrador_cp + 2)

        setRegistrador(operador1, getRegistrador(operador1) + operador2)

    elif idInstrucao == OPCODES['add_reg_reg']:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)
        operador2 = memoria.getValorMemoria(registrador_cp + 2)

        setRegistrador(operador1, getRegistrador(operador1) + getRegistrador(operador2))

    elif idInstrucao == OPCODES["inc"]:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)

        setRegistrador(operador1, getRegistrador(operador1) + 1)

    elif idInstrucao == OPCODES["dec"]:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)

        setRegistrador(operador1, getRegistrador(operador1) - 1)

    elif idInstrucao == OPCODES["sub_reg_byte"]:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)
        operador2 = memoria.getValorMemoria(registrador_cp + 2)
        
        setRegistrador(operador1, getRegistrador(operador1) - operador2)

    elif idInstrucao == OPCODES["sub_reg_reg"]:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)
        operador2 = memoria.getValorMemoria(registrador_cp + 2)
        
        setRegistrador(operador1, getRegistrador(operador1) - getRegistrador(operador2))

    elif idInstrucao == OPCODES["mov_reg_byte"]:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)
        operador2 = memoria.getValorMemoria(registrador_cp + 2)
        
        setRegistrador(operador1, operador2)

    elif idInstrucao == OPCODES["mov_reg_reg"]:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)
        operador2 = memoria.getValorMemoria(registrador_cp + 2)
        
        setRegistrador(operador1, getRegistrador(operador2))

    elif idInstrucao == OPCODES["jmp"]:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)

        setRegistrador(OPCODES["cp"], operador1)

    elif idInstrucao == OPCODES["cmp_reg_byte"]:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)
        operador2 = memoria.getValorMemoria(registrador_cp + 2)

        value_reg = getRegistrador(operador1)
        result = value_reg - operador2

        if result == 0:
            flag_zero = 1
        else:
            flag_zero = 0
        
    elif idInstrucao == OPCODES["cmp_reg_reg"]:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)
        operador2 = memoria.getValorMemoria(registrador_cp + 2)

        value_reg1 = getRegistrador(operador1)
        value_reg2 = getRegistrador(operador2)

        result = value_reg1 - value_reg2

        if result == 0:
            flag_zero = 1
        else:
            flag_zero = 0

    elif idInstrucao == OPCODES["jz"] or idInstrucao == OPCODES["jz_bug"]:
        operador1 = memoria.getValorMemoria(registrador_cp + 1)

        if flag_zero == 1:
            setRegistrador(OPCODES["cp"], operador1)


def calcularProximaInstrucao(idInstrucao):
    global registrador_cp
    global flag_zero

    if idInstrucao == OPCODES["add_reg_byte"]:
        registrador_cp += 3

    elif idInstrucao == OPCODES["add_reg_reg"]:
        registrador_cp += 3

    elif idInstrucao == OPCODES["inc"]:
        registrador_cp += 2

    elif idInstrucao == OPCODES["dec"]:
        registrador_cp += 2

    elif idInstrucao == OPCODES["sub_reg_byte"]:
        registrador_cp += 3

    elif idInstrucao == OPCODES["sub_reg_reg"]:
        registrador_cp += 3

    elif idInstrucao == OPCODES["mov_reg_byte"]:
        registrador_cp += 3
    
    elif idInstrucao == OPCODES["mov_reg_reg"]:
        registrador_cp += 3

    elif idInstrucao == OPCODES["jmp"]:
        registrador_cp += 0
    
    elif idInstrucao == OPCODES["cmp_reg_byte"]:
        registrador_cp += 3
    
    elif idInstrucao == OPCODES["cmp_reg_reg"]:
        registrador_cp += 3

    elif idInstrucao == OPCODES["jz"]:
        if flag_zero == 1:
            registrador_cp += 0
        else:
            registrador_cp += 2


def dumpRegistradores():
    if CPU_DEBUG:
        print(f'CP[{registrador_cp:02X}] \
            AX[{registrador_ax:02X}]  \
            BX[{registrador_bx:02X}]  \
            CX[{registrador_cx:02X}]  \
            DX[{registrador_dx:02X}]  \
            ZF[{flag_zero}] ')

if __name__ == '__main__':
    while (True):

        if registrador_cp < memoria.getTamanhoMemoria():
            #Unidade de Controle
            idInstrucao = buscarEDecodificarInstrucao()

            #ULA
            lerOperadoresExecutarInstrucao(idInstrucao)  

            dumpRegistradores() 

            #Unidade de Controle
            calcularProximaInstrucao(idInstrucao)

            #apenas para nao ficar em loop voce pode comentar a linha abaixo =)
            sys.stdin.read(1)

        else:
            dumpRegistradores()
            print("Fim ;D")
            sys.stdin.read(1)
