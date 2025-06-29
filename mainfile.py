#Autor: Daniel Castro
#Github: github.com/danielbirenbaum
from colors import Color as C
import time
from datetime import datetime
import csv
import os
import tabulate # type: ignore

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
#OTIMIZADO
def isEmpty(header,items):
    if len(items) == 0: return True
    else: return False
#OTIMIZADO
def expirationWarning(header,items):
    current = datetime.now()
    #Linha pode parecer confusa, mas significa o seguinte:
    #Para cada item na geladeira, vou colocar na lista o nome deste item como primeiro elemento e a quantidade de dias para vencer no segundo elemento
    #isso é feito utilizando-se de alguns passos:
    #o construtor datetime() vai instanciar um objeto do tipo datetime que pode ser usado para manipular tempo de maneira mais precisa
    #depois vou subtrarir o current que seria o momento atual
    #.days() irá pegar a quantidade de dias na diferença
    #+1 apenas serve para fazer com que a diferença seja mais correta, ou seja, quando é falado uma data (linguisticamente)
    listNamesAndExp = [[i[0],(datetime(int(i[2][4:]),int(i[2][2:4]),int(i[2][0:2])) - current).days + 1] for i in items]
    for i in listNamesAndExp:
        if i[1] <= 3:
            print(C.FAIL + "ALERTA, ALIMENTO(S) PRÓXIMO(S) DA VALIDADE:")
            break
    for i in listNamesAndExp:
        if i[1] <= 3 and i[1] > 0: 
            print(f"{i[0]} vence em {i[1]} dia(s)")
        if i[1] == 0:
            print(f"{i[0]} com prazo de validade hoje!")
        if i[1] < 0:
            print(f"{i[0]} venceu há {(-1)*i[1]} dia(s)")                 
#OTIMIZADO
def getName(name):
    nome = input(C.OKCYAN + "Digite o nome do produto:\n>>> " + C.ENDC).strip()
    if not nome:
        print(C.FAIL + "DIGITE UM NOME!" + C.ENDC)
        time.sleep(0.8)
        clearT()
        return False
    else: return nome
def quantityType(quantificavel):
    print(C.OKCYAN + "Produto medido em gramatura ou em quantidade?")
    print("1 - Gramas\n2 - Quantidade\n3 - Mililitros" + C.ENDC)
    quantificavel = getValidInput(C. OKCYAN + ">>> " + C.ENDC ,int, C.FAIL + "DIGITE 1, 2 ou 3" + C.ENDC)
    if quantificavel not in [1,2,3]:
        print(C.FAIL + "DIGITE 1, 2 ou 3" + C.ENDC)
        time.sleep(0.8)
        clearT()
        return False
    else: return quantificavel
def getQuantity(quantidade,quantificavel,nome):
    unidade = ["gramas", "itens", "mililitros"][quantificavel - 1]
    quantidade = getValidInput(C.OKCYAN + f"Quantos {unidade} de {nome}?\n>>> " + C.ENDC, int if quantificavel == 2 else float)
    if quantidade <= 0:
        print(C.FAIL + f"NÃO É POSSÍVEL COLOCAR ESSA QUANTIDADE DE {unidade.upper()}" + C.ENDC)
        time.sleep(0.8)
        quantidade = 0
        return False
    else: return quantidade
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
                nome = getName(nome)
                if not nome: continue
            if not quantificavel:
                quantificavel = quantityType(quantificavel)
                if not quantificavel: continue
            if not quantidade:
                quantidade = getQuantity(quantidade,quantificavel,nome)
                if not quantidade: continue
            if not boolValidade:
                #Datas de acordo com os padrões da ABNT, norma NBR 5892:2019/ISO 8601-2-2019
                #Não são utilizados os hífens (-) no csv para evitar erros de leitura
                print(C.OKGREEN + f"Digite a validade do produto:\nPara meses e dias menores que 10, digite com um zero à esquerda, por exemplo:\nDia: 03\nMes: 09\nAno: 2025{C.ENDC}")
                dia = getValidInput(C.OKCYAN + "Dia:\n>>> " + C.ENDC, str)
                mes = getValidInput(C.OKCYAN + "Mês:\n>>> " + C.ENDC, str)
                ano = getValidInput(C.OKCYAN +"Ano:\n>>> " + C.ENDC, str)
                date = f"{dia}{mes}{ano}"
                datetime(int(ano),int(mes),int(dia))
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

            return header,items
        except IndexError as ind:
            print(C.FAIL + f"Erro: {ind}" + C.ENDC)
        except ValueError as vE:
            print(C.FAIL + f"INPUT INVÁLIDO, POR FAVOR TENTE NOVAMENTE: {vE}" + C.ENDC)
            time.sleep(0.8)
            clearT()
        except KeyboardInterrupt:
            print("")
            print(C.FAIL + "RETORNANDO AO MENU PRINCIPAL..." + C.ENDC)
            return True
#OTIMIZADO 
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
            #items.pop(index)
            quantity = getValidInput(C.OKGREEN + f"Digite a quantidade a ser {C.FAIL}removido:\n{C.ENDC}{C.OKGREEN}>>> " + C.ENDC,int if items[index][3] == '1' else float ,C.FAIL + "DIGITE UM VALOR VÁLIDO" + C.ENDC)
            
            if (float(items[index][1]) - quantity < 0 or quantity <= 0): raise ValueError
            elif float(items[index][1]) - quantity == 0: items.pop(index)
            else: 
                if (items[index][3] == '1'): items[index][1] = str(int(items[index][1]) - quantity)
                else: items[index][1] = str(float(items[index][1]) - quantity)
        
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
    table = tabulate.tabulate(listOfExpiration,headers=newHeaderE, tablefmt= "pipe", colalign=('center','center','center', 'center'))
    print(C.WARNING + table + C.ENDC)
    return header,items
#OTIMIZADO: FUNÇÃO RESPONSÁVEL POR LER OS DADOS DO ARQUIVO
def readFile(header,items):
    with open("data/data.csv", mode = 'r', encoding='utf-8') as data:
        reader = csv.reader(data)
        header = tuple(next(reader))
        for row in reader:
            items.append(row)
    return header,items
#OTIMIZADO
def writeInFile(header,items):
    data = []
    data.append(list(header))
    for i in items:
        data.append(i)
    with open("data/data.csv",mode='w',newline='',encoding='utf-8') as fileData:
        writer = csv.writer(fileData)
        writer.writerows(data)
#OTIMIZADO
def finish(header,items):
    clearT()
    print(C.FAIL + "FECHANDO.." + C.ENDC)
    time.sleep(0.8)
    clearT()
    return 'G7f#Lp29$Xq!dRb'
#Funcao principal
def main(): 
    #A key é uma forma de saber quando o código deve ser finalizado
    #Utilizado pois inicialmente eu havia pensado em usar boleanos, mas depois percebi que o uso de boleanos poderia ser aplicado em outra coisa
    key = 'G7f#Lp29$Xq!dRb'
    #Uso do dicionário (map) ao invés de vários if statements, torna o código mais nobre
    choice = {
        1: insert,
        2: remove,
        3: getProducts,
        4: getExpirationDate,
        5: finish
    }
    header = ()
    items = []
    #Apesar de 'items' ser "passado por referência", 'header' é uma tupla, logo modificar 'header' em uma função não a modificará aqui
    #Deixo o fato de 'items' ser 'passado por referência' aqui explícito, pois foi algo amplamente usado no código
    #'items' é modificado nas funções e eu não me preocupo com o escopo, logo, ele é modificado aqui também
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
                print("5 - Sair do programa")
                c = getValidInput(C.OKGREEN + ">>> " + C.ENDC,int,C.FAIL + "ESCOLHA VALORES INTEIROS ENTRE 1 E 5" + C.ENDC)  
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
        #Ao final do código, há o update no arquivo .csv
        #Em tempo de execução, não há atualizações constantes no arquivo. Há apenas a manipulação de dados conforme visto em aula
        writeInFile(header,items)
    
    except FileExistsError:
        return print(C.FAIL + f"ARQUIVO DE DADOS JÁ EXISTENTE (SOBREPOSIÇÃO):" + C.ENDC)
    
    except FileNotFoundError:
        return print(C.FAIL + f"ARQUIVO DE DADOS INEXISTENTE:" + C.ENDC)
    
    except Exception as e:
        return print(C.FAIL + f"UNEXPECTED ERROR, PLEASE RESTART THE SYSTEM: {e}" + C.ENDC)
        
if __name__ == '__main__':
    main()