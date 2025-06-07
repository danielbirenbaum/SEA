from colors import Color as C
import time
from datetime import datetime
import csv
import os
import tabulate # type: ignore
import platform

#Funcao para pegar um input e tratá-lo
def getValidInput(prompt,inputType,errorMessage = "Entrada Inválida"):
    while True:
        try:
            value = input(prompt)
            return inputType(value)
        except ValueError:
            print(errorMessage)
            time.sleep(0.8)

# Função para limpar o terminal, independente do sistema (não funciona direito ainda)
def clearT():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

#Verifica se há uma linha vazia para poder escrever uma nova linha
def verifyFile():
    with open('data/data.csv', mode = 'r+', encoding='utf-8') as data:
        content = data.read()
        if not content.endswith('\n'):
            data.write("\n")

def isEmpty():
    with open('data/data.csv', mode = 'r') as data:
        c = 0
        csvReader = csv.reader(data)
        header = next(csvReader)
        for i in csvReader:
            c += 1
        if (c == 0):
            return True

def expirationWarning():
    with open('data/data.csv', mode = 'r', encoding='utf-8') as data:
        listOfAllContent = []
        remainingTime = []
        csvReader = csv.reader(data)
        headerData = next(csvReader)
        for row in csvReader:
            listOfAllContent.append(row)     
        for i in listOfAllContent:
            name = i[0]
            dia = int(i[2][0:2])
            mes = int(i[2][2:4])
            ano = int(i[2][4:])
            eDate = datetime(ano, mes, dia)
            currentDate = datetime.now()
            dif = eDate - currentDate
            remainingTime.append([name,dif.days + 1]) 
        for i in remainingTime:
            if i[1] <= 3:
                print(C.FAIL + "ALERTA, ALIMENTO(S) PRÓXIMO DA VALIDADE:")
                break
            
        for i in remainingTime:
            if i[1] <= 3 and i[1] > 0: 
                print(f"{i[0]} vence em {i[1]} dia(s)")
            if i[1] == 0:
                print(f"{i[0]} com prazo de validade hoje!")
            if i[1] < 0:
                print(f"{i[0]} venceu há {(-1)*i[1]} dia(s)")
        print(C.ENDC)
                  

def insert():
    verifyFile()
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
                quantidade = getValidInput(C.OKCYAN + f"Quantos {unidade} de {nome}?\n>>> " + C.ENDC, float if quantificavel == 1 else int)
                if quantidade <= 0:
                    print(C.FAIL + f"NÃO É POSSÍVEL COLOCAR ESSA QUANTIDADE DE {unidade.upper()}" + C.ENDC)
                    time.sleep(0.8)
                    quantidade = 0
                    continue
            if not boolValidade:
                print(C.OKCYAN + "Agora insira a data de validade do produto:" + C.ENDC)
                print(C.OKGREEN + "Dia:" + C.ENDC)
               
                dia = (input(">>> "))
                print(C.OKGREEN + "Mês:" + C.ENDC)
                mes = (input(">>> "))
                print(C.OKGREEN + "Ano:" + C.ENDC)
                ano = (input(">>> "))
                date = str(dia) + str(mes) + str(ano)
                boolValidade = True
            
            if boolValidade and nome and quantidade and quantificavel:
                newRow.append(str(nome))
                newRow.append(str(quantidade))
                newRow.append(str(date))
                newRow.append(str(quantificavel - 1))
                count = 0
                with open('data/data.csv', mode='r', encoding='utf-8') as data:
                    csvReader = csv.reader(data)
                    header = next(csvReader)
                    listOfAllContent = []
                    for row in csvReader:
                        listOfAllContent.append(row)
                    for i in listOfAllContent:
                        count = int(i[4])
                newRow.append(str(count + 1))
                with open('data/data.csv', mode = 'a', encoding='utf-8', newline='') as data:
                    writer = csv.writer(data, delimiter=',')
                    writer.writerow(newRow)
                    
            
            break
        except ValueError:
            print(C.FAIL + "INPUT INVÁLIDO, POR FAVOR TENTE NOVAMENTE" + C.ENDC)
            time.sleep(0.8)
            clearT()
        except KeyboardInterrupt:
            print("")
            print(C.FAIL + "RETORNANDO AO MENU PRINCIPAL..." + C.ENDC)
            return

def remove():
    if isEmpty(): return print(C.FAIL + "GELADEIRA VAZIA" + C.ENDC)
    name = False
    quantity = False
    remainingQnt = False
    listOfAllContent = []
    equalName = []
    listId = []
    rowToRemove = []
    newFile = []
    header = []
    count = 0
    while True:
        try:
            if not name:
                print(C.OKGREEN + f"Digite o nome do produto a ser {C.FAIL}removido{C.ENDC}:" + C.ENDC)
                value = input(">>> ")
                if value == "":
                    print(C.FAIL + "DIGITE UM NOME VÁLIDO!" + C.ENDC)
                    continue
                else:
                    name = value
                    with open('data/data.csv', 'r', encoding='utf-8') as data:
                        csvReader = csv.reader(data)
                        header = next(csvReader) 
                        nameExist = False 
                        for row in csvReader:
                            listOfAllContent.append(row)
                            if row[0] == name:
                                quantity = row[1]
                                nameExist = True
                                count += 1
                                equalName.append([row[0],row[1],row[2],row[4]])
                                listId.append(row[4])
                                rowToRemove.append(row)
            #Falta terminar funcionalidade de remover alguma quantidade
            #Código muito mal otimizado
            if not(remainingQnt):
                print(C.OKGREEN + f"Temos {quantity} de {name}, quanto deve ser {C.FAIL}removido{C.ENDC}?" + C.ENDC)
                value = float(input(">>> "))   
                remainingQnt = float(quantity) - value       
            if count > 1:
                table = tabulate.tabulate(equalName ,headers=['Nome','Quantidade', 'Validade', 'ID'], tablefmt= "pipe", colalign=('center','center','center','center'))
                print(C.WARNING + table + C.ENDC)
                print("")
                
                print(C.OKGREEN + "Digite o ID do produto que deseja remover:" + C.ENDC)
                idValue = int(input(">>> "))
                if str(idValue) not in listId:
                    print(C.FAIL + "DIGITE UM ID VÁLIDO" + C.ENDC)
                    continue
                else:
                    print(f"{C.FAIL}Removendo{C.ENDC} {C.OKGREEN}{name}{C.ENDC}")
                    for i in rowToRemove:
                        if i[4] == str(idValue):
                            rowToRemove = []
                            rowToRemove.append(i)
                    newFile = [row for row in listOfAllContent if rowToRemove[0][4] not in row[4]]
                    newFile.insert(0,header)
                    
                    with open("data/data.csv", "w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(newFile)
                    return

            else:
                print(f"{C.FAIL}Removendo{C.ENDC} {C.OKGREEN}{name}{C.ENDC}")
                newFile = [row for row in listOfAllContent if rowToRemove[0][4] not in row[4]]
                newFile.insert(0,header)                   
                with open("data/data.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(newFile)
                return
            
                    

        except ValueError:
            print(C.FAIL + "INPUT INVÁLIDO, POR FAVOR TENTE NOVAMENTE" + C.ENDC)
            time.sleep(0.8)
            clearT()
        except KeyboardInterrupt:
            print("")
            print(C.FAIL + "RETORNANDO AO MENU PRINCIPAL..." + C.ENDC)
            return
        except IndexError:
            print("")
            clearT()
            print(C.FAIL + "RETORNE E DIGITE UM VALOR VÁLIDO" + C.ENDC)
            time.sleep(1)
            clearT()
            return

def getProducts():
    if isEmpty():
        print(C.FAIL + "GELADEIRA VAZIA" + C.ENDC)
        return

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

        table = tabulate.tabulate(listOfNamesAndQnt,headers=header, tablefmt= "pipe", colalign=('center','center'))
        print(C.WARNING + table + C.ENDC)


def getExpirationDate():
    if isEmpty():
        print(C.FAIL + "GELADEIRA VAZIA" + C.ENDC)
        return
    
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
            
        
        table = tabulate.tabulate(listOfExpiration,headers=header, tablefmt= "pipe", colalign=('center','center','center', 'center'))
        print(C.WARNING + table + C.ENDC)

def getRoutine():
    pass

def getList():
    pass

def main(): 
    online = True
    while online:
        print(C.OKBLUE + "BEM-VINDO AO SISTEMA DE ESTOQUE AUTOMÁTICO" + C.ENDC)
        print("")
        expirationWarning()
        print(C.OKGREEN + "Escolha uma opção:"+ C.ENDC)
        print("1 - Inserir")
        print("2 - Remover")
        print("3 - Produtos")
        print("4 - Validades")
        print("5 - Rotina")
        print("6 - Gerar lista")
        print("7 - Sair do programa")
        choice = input(">>> ")
        
        
        if choice == '7':
            clearT()
            print(C.FAIL + "FECHANDO.." + C.ENDC)
            time.sleep(0.8)
            clearT()
            online =  False
        elif choice == '1':
            clearT()
            insert()
            print("")
            print("Pressione enter para continuar")
            input(">>> ")
            clearT()
        
        elif choice == '2':
            clearT()
            remove()
            print("")
            print("Pressione enter para continuar")
            input(">>>")
            clearT()
        elif choice == '3':
            clearT()
            getProducts()
            print("")
            print("Pressione enter para continuar")
            input(">>> ")
            clearT()

        elif choice == '4':
            clearT()
            getExpirationDate()
            print("")
            print("Pressione enter para continuar")
            input(">>> ")
            clearT()            
        elif choice == '5':
            getRoutine()
        elif choice == '6':
            getList()
        else:
            print(C.FAIL + "ERRO:")
            print("ESCOLHA UMA OPÇÃO VÁLIDA" + C.ENDC)
            time.sleep(1)
            clearT()
        

if __name__ == '__main__':
    main()