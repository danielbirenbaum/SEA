from colors import Color as C
import time
from datetime import datetime
import csv
import os
import tabulate # type: ignore
import platform

#Funcao para pegar um input e tratá-lo
#O tratamento NÃO É ESPECIAL, há apenas a verificação do tipo, logo, pode ser necessário verificar outros fatores
def getValidInput(prompt,inputType,errorMessage = C.FAIL + "ENTRADA INVALIDA" + C.ENDC):
    while True:
        try:
            value = input(prompt)
            return inputType(value)
        except ValueError:
            print(errorMessage)
            time.sleep(0.8)
# Função para limpar o terminal (Apenas windows)
def clearT():
    os.system('cls')
'''
#Verifica se há uma linha vazia para poder escrever uma nova linha(código estava escrevendo na mesma linha)
def verifyFile():
    with open('data/data.csv', mode = 'r+', encoding='utf-8') as data:
        content = data.read()
        if not content.endswith('\n'):
            data.write("\n")
'''
#OTIMIZADO
def isEmpty(header,items):
    if len(items) == 0: return True
    else: return False
#OTIMIZADO
def expirationWarning(header,items):
    current = datetime.now()
    listNamesAndExp = [[i[0],(datetime(int(i[2][4:]),int(i[2][2:4]),int(i[2][0:2])) - current).days + 1] for i in items]
    #remainingT = [i[1].days + 1 for i in listNamesAndExp]
    for i in listNamesAndExp:
        if i[1] <= 3:
            print(C.FAIL + "ALERTA, ALIMENTO(S) PRÓXIMO DA VALIDADE:")
            break
    for i in listNamesAndExp:
        if i[1] <= 3 and i[1] > 0: 
            print(f"{i[0]} vence em {i[1]} dia(s)")
        if i[1] == 0:
            print(f"{i[0]} com prazo de validade hoje!")
        if i[1] < 0:
            print(f"{i[0]} venceu há {(-1)*i[1]} dia(s)")                 
#OTIMIZADO
def insert(header,items):
    nome = False
    quantidade = False
    boolValidade = False
    quantificavel = False
    date = ""
    newRow = []
    while True:
        try:
            if not nome:
                nome = input(C.OKCYAN + "Digite o nome do produto:\n>>> " + C.ENDC).strip()
                if not nome:
                    print(C.FAIL + "DIGITE UM NOME!" + C.ENDC)
                    time.sleep(0.8)
                    clearT()
                    continue
            if not quantificavel:
                print(C.OKCYAN + "Produto medido em gramatura ou em quantidade?")
                print("1 - Gramas\n2 - Quantidade\n3 - Mililitros" + C.ENDC)
                quantificavel = getValidInput(C. OKCYAN + ">>> " + C.ENDC ,int, C.FAIL + "DIGITE 1, 2 ou 3" + C.ENDC)
                if quantificavel not in [1,2,3]:
                    quantificavel = False
                    print(C.FAIL + "DIGITE 1, 2 ou 3" + C.ENDC)
                    time.sleep(0.8)
                    clearT()
                    continue
            if not quantidade:
                unidade = ["gramas", "itens", "mililitros"][quantificavel - 1]
                quantidade = getValidInput(C.OKCYAN + f"Quantos {unidade} de {nome}?\n>>> " + C.ENDC, int if quantificavel == 2 else float)
                if quantidade <= 0:
                    print(C.FAIL + f"NÃO É POSSÍVEL COLOCAR ESSA QUANTIDADE DE {unidade.upper()}" + C.ENDC)
                    time.sleep(0.8)
                    quantidade = 0
                    continue
            if not boolValidade:
                dia = getValidInput(C.OKCYAN + "Dia:\n>>> " + C.ENDC, str)
                mes = getValidInput(C.OKCYAN + "Mês:\n>>> " + C.ENDC, str)
                ano = getValidInput(C.OKCYAN +"Ano:\n>>> " + C.ENDC, str)
                date = f"{dia}{mes}{ano}"
                boolValidade = True
        
            newRow.append(str(nome))
            newRow.append(str(quantidade))
            newRow.append(str(date))
            newRow.append(str(quantificavel - 1))
            countId = 0
            for i in items:
                if int(i[4]) >= countId:
                    countId = int(i[4]) + 1
            newRow.append(str(countId))
            items.append(newRow)
            '''
            with open('data/data.csv', mode='r', encoding='utf-8') as data:
                csvReader = csv.reader(data)
                header = next(csvReader)
                listOfAllContent = []
                for row in csvReader:
                    listOfAllContent.append(row)
                for i in listOfAllContent:
                    if (count < int(i[4])):
                        count = int(i[4])
            newRow.append(str(count + 1))
            with open('data/data.csv', mode = 'a', encoding='utf-8', newline='') as data:
                writer = csv.writer(data, delimiter=',')
                writer.writerow(newRow)
            '''     
            return header,items
        except IndexError as ind:
            print(C.FAIL + f"Erro: {ind}" + C.ENDC)
        except ValueError:
            print(C.FAIL + "INPUT INVÁLIDO, POR FAVOR TENTE NOVAMENTE" + C.ENDC)
            time.sleep(0.8)
            clearT()
        except KeyboardInterrupt:
            print("")
            print(C.FAIL + "RETORNANDO AO MENU PRINCIPAL..." + C.ENDC)
            return True
#OTIMIZADO -> NECESSITA AINDA ADICIONAR A OPÇÃO DE REMOÇÃO PARCIAL
def remove(header,items):
    if isEmpty(header,items): 
        print(C.FAIL + "GELADEIRA VAZIA" + C.ENDC)
        return header,items
    print(C.OKGREEN + "PRODUTOS DISPONÍVEIS: \n" + C.ENDC)
    getProducts(header,items)
    print("")
    try:    
        while True:
            idList = [int(i[4]) for i in items]
            removeId = getValidInput(C.OKGREEN + f"Digite o ID do produto a ser {C.FAIL}removido:\n{C.ENDC}{C.OKGREEN}>>> " + C.ENDC,int,C.FAIL + "DIGITE UM INTEIRO QUE REPRESENTE UM ID" + C.ENDC)
            if removeId not in idList:
                print(C.FAIL + "DIGITE UM ID DISPONÍVEL" + C.ENDC)
                time.sleep(0.8)
                continue
            index = idList.index(removeId)
            items.pop(index)
            if not isEmpty(header,items):
                keep = getValidInput(C.OKGREEN + f"Pressione qualquer tecla para sair, digite {C.FAIL}(r){C.ENDC}{C.OKGREEN} para continuar {C.FAIL}removendo{C.ENDC}{C.OKGREEN}:\n>>> " + C.ENDC, str)
                if keep == 'r':
                    print("")
                    getProducts(header,items)
                    print("")
                    continue
            
            return header,items

    except ValueError:
        print(C.FAIL + "INPUT INVÁLIDO, POR FAVOR TENTE NOVAMENTE" + C.ENDC)
        time.sleep(0.8)
        clearT()
    except KeyboardInterrupt:
        print("")
        print(C.FAIL + "RETORNANDO AO MENU PRINCIPAL..." + C.ENDC)
        return True
    except IndexError:
        print("")
        clearT()
        print(C.FAIL + "RETORNE E DIGITE UM VALOR VÁLIDO" + C.ENDC)
        time.sleep(1)
        clearT()
        return True
#OTIMIZADO
def getProducts(header,items):
    if isEmpty(header,items):
        print(C.FAIL + "GELADEIRA VAZIA" + C.ENDC)
        return header,items
    newHeaderP = (header[0], header[1], header[4])
    listOfNamesAndQnt = []
    poss = ['gramas','itens','mililitros']
    for i in items:
        listOfNamesAndQnt.append([i[0],i[1] + f" {poss[int(i[3])]}",i[4]])
    '''
    with open('data/data.csv', mode = 'r', encoding='utf-8') as data:
        listOfAllContent = []
        listOfNamesAndQnt = []
        csvReader = csv.reader(data)
        header = next(csvReader)
        for row in csvReader:
            listOfAllContent.append(row)
                
        for i in listOfAllContent:
            l = []
            l.append(i[0]) 
            if i[3] == '1':
                if int(i[1]) == 1:
                    l.append(f'{i[1]} item')
                else:
                    l.append(f'{i[1]} itens')
            elif i[3] == '0':
                l.append(f'{i[1]} gramas')
            else:
                l.append(f'{i[1]} mililitros')

            listOfNamesAndQnt.append(l)
    '''
    table = tabulate.tabulate(listOfNamesAndQnt,headers=newHeaderP, tablefmt= "pipe", colalign=('center','center'))
    print(C.WARNING + table + C.ENDC)
    return header,items
#OTIMIZADO
def getExpirationDate(header,items):
    if isEmpty(header,items):
        print(C.FAIL + "GELADEIRA VAZIA" + C.ENDC)
        return
    newHeaderE = (header[0],"Dia","Mês","Ano",header[4])
    listOfExpiration = [[i[0],i[2][0:2],i[2][2:4],i[2][4:],i[4]] for i in items]
    '''
    with open('data/data.csv', mode = 'r', encoding='utf-8') as data:
        listOfAllContent = []
        listOfExpiration = []
        csvReader = csv.reader(data)
        headerData = next(csvReader)
        header = ["Nome","Dia", "Mês", "Ano"]
        
        for row in csvReader:
            listOfAllContent.append(row)
              
        for i in listOfAllContent:
            l = []
            nome = i[0]
            dia = i[2][0:2]
            mes = i[2][2:4]
            ano = i[2][4:]
            l.append(nome)
            l.append(dia)
            l.append(mes)
            l.append(ano)
            listOfExpiration.append(l)
            
        '''
    table = tabulate.tabulate(listOfExpiration,headers=newHeaderE, tablefmt= "pipe", colalign=('center','center','center', 'center'))
    print(C.WARNING + table + C.ENDC)
    return header,items

def getRoutine():
    pass

def getList():
    pass

#FUNÇÃO RESPONSÁVEL POR LER OS DADOS DO ARQUIVO
def readFile(header,items):
    with open("data/data.csv", mode = 'r', encoding='utf-8') as data:
        reader = csv.reader(data)
        header = tuple(next(reader))
        for row in reader:
            items.append(row)
    return header,items
#FUNÇÃO QUE SERÁ RESPONSÁVEL POR GRAVAR, AO FINAL DO PROGRAMA, TODOS OS NOVOS DADOS
def writeInFile():
    pass

def finish(header,items):
    clearT()
    print(C.FAIL + "FECHANDO.." + C.ENDC)
    time.sleep(0.8)
    clearT()
    return 'G7f#Lp29$Xq!dRb'

#Função mais mais limpa com a utilização de dicionário para controle de chamada de função
#Reformulação do código: menos acessos a memória não-volátil
def main(): 
    #A key é uma forma de saber quando o código deve ser finalizado
    key = 'G7f#Lp29$Xq!dRb'
    choice = {
        1: insert,
        2: remove,
        3: getProducts,
        4: getExpirationDate,
        5: getRoutine,
        6: getList,
        7: finish
    }
    header = ()
    items = []
    header,items = readFile(header,items)
    try:
        while True:
            try: 
                print(C.OKBLUE + "BEM-VINDO AO SISTEMA DE ESTOQUE AUTOMÁTICO" + C.ENDC)
                print("")
                expirationWarning(header,items)
                print("")
                print(C.OKGREEN + "Escolha uma opção:"+ C.ENDC)
                print("1 - Inserir")
                print("2 - Remover")
                print("3 - Produtos")
                print("4 - Validades")
                print("5 - Rotina")
                print("6 - Gerar lista")
                print("7 - Sair do programa")
                c = getValidInput(C.OKGREEN + ">>> " + C.ENDC,int,C.FAIL + "ESCOLHA VALORES INTEIROS ENTRE 1 E 7" + C.ENDC)
                
                clearT()
                value = choice[c](header,items)
                if value == key: break
                else:
                    print("")
                    print("Pressione enter para continuar")
                    input(">>> ")
                    clearT()

            except KeyError:
                print(C.FAIL + "ESCOLHA UMA OPÇÃO VÁLIDA" + C.ENDC)
                time.sleep(1)
                clearT()
                continue  
            except KeyboardInterrupt:
                return print(C.FAIL + "FORÇANDO PARADA..." + C.ENDC) 
    
    except FileNotFoundError:
        return print(C.FAIL + f"ARQUIVO DE DADOS INEXISTENTE:" + C.ENDC)
    
    except Exception as e:
        return print(C.FAIL + f"UNEXPECTED ERROR, PLEASE RESTART THE SYSTEM: {e}" + C.ENDC)
        
if __name__ == '__main__':
    main()