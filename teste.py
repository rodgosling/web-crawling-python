import ast

file = open ("teste.txt", "w")
nome = 'rodrigo'
data = 31
mes = 1
signo = 'aquario'

lista = [nome, data, mes, signo]
listast = str (lista)

file.write (listast)

file = open ("teste.txt", "r")

leitura = file.readline ()

leiturast = str (leitura)

limpeza = ast.literal_eval (leiturast)

limpezalst = list (limpeza)

nomelst = limpezalst [0]

nome2 = input ("digite: ")


if nomelst == nome2:
    print ("iés")

else:
    print ("cu do capeta")
    
file.close
           
