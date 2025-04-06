from colors import Color as C
import time
import csv
import os
import tabulate

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
    pass

def insert():
    pass

def remove():
    pass

def getProducts():
    if isEmpty():
        print(C.FAIL + "GELADEIRA VAZIA" + C.ENDC)
        return

    with open('data/data.csv', mode = 'r') as data:
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
                l.append(f'{i[1]} itens')
            else:
                l.append(f'{i[1]} gramas')
            listOfNamesAndQnt.append(l)

        table = tabulate.tabulate(listOfNamesAndQnt,headers=header, tablefmt= "pipe", colalign=('center','center'))
        print(C.WARNING + table + C.ENDC)


def getExpirationDate():
    if isEmpty():
        print(C.FAIL + "GELADEIRA VAZIA" + C.ENDC)
        return
    
    with open('data/data.csv', mode = 'r') as data:
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
            
        
        table = tabulate.tabulate(listOfExpiration,headers=header, tablefmt= "pipe", colalign=('center','center','center'))
        print(C.WARNING + table + C.ENDC)

def getRoutine():
    pass

def getList():
    pass

def main():
    online = True
    while online:
        print(C.OKBLUE + "BEM-VINDO AO SISTEMA DE ESTOQUE AUTOMÁTICO" + C.ENDC)
        expirationWarning()
        print("")
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
            os.system('cls')
            print(C.FAIL + "FECHANDO.." + C.ENDC)
            time.sleep(0.8)
            os.system('cls')
            online =  False
        elif choice == '1':
            insert()
        
        elif choice == '2':
            remove()

        elif choice == '3':
            os.system('cls')
            getProducts()
            print("")
            print("Pressione enter para continuar")
            input(">>> ")
            os.system('cls')

        elif choice == '4':
            os.system('cls')
            getExpirationDate()
            print("")
            print("Pressione enter para continuar")
            input(">>> ")
            os.system('cls')            
        elif choice == '5':
            getRoutine()
        elif choice == '6':
            getList()
        else:
            print(C.FAIL + "ERRO:")
            print("ESCOLHA UMA OPÇÃO VÁLIDA" + C.ENDC)
            time.sleep(1)
            os.system('cls')
        
        


if __name__ == '__main__':
    main()