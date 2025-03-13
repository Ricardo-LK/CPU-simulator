import sys

class MemoriaCache:

    def __init__(self, arquivo):
        self.__memoria = []
        print('Abrindo arquivo de memoria: ' + arquivo)
        try:
            with open(arquivo, "rb") as f:
                while (byte := f.read(1)):
                    print(f'Cache[{len(self.__memoria)}]: {byte.hex()}')
                    self.__memoria.append(byte)
            print(self.__memoria)
            #self.__memoria = bytearray(self.__memoria)
        except Exception as e:
            print('Erro na leitura do arquivo: ' + arquivo)
            print(e)
            sys.exit(-1)
        self.__tamanho = len(self.__memoria)
    
    def carregaArquivo(self, arquivo):
        print(arquivo)

    def getTamanhoMemoria(self):
        return self.__tamanho

    def getValorMemoria(self, endereco):
        if endereco >= len(self.__memoria):
            print('Voce tentou acessar um endereco de memoria invalido, programa encerrou?')
            sys.exit(1)
        return int.from_bytes(self.__memoria[endereco], "big")
    
    def setValorMemoria(self, endereco, valor):
        self.__memoria[endereco] = valor