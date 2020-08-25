"""

Um pequeno script Python que roda na propria maquina, que faz o seguinte
1 - Atraves de um menu pergunta o dia e mês que a pessoa nasceu e dá o signo
2 - Guarda o signo num arquivo texto para referencia futura (porem no menu 1 tem que ter a opção de trocar)
3 - Busca na web o horoscopo dessa pessoa no dia
http://somostodosum.ig.com.br/horoscopo/
http://www1.folha.uol.com.br/horoscopo/
http://extra.globo.com/horoscopo/

   
"""

# Módulos

import ast                                          # Módulo para limpar lista gerada a partir do arquivo txt 
from bs4 import BeautifulSoup                       # Módulo para retirar somente o texto de um html
from urllib.request import urlopen                  # Módulo para abrir urls


def main():

    global signo_url                                
    
    nome = input ("Digite seu nome: ")
    
    # Abrindo arquivo de gravação e fazendo a leitura dos dados salvos
    file = open ("data.txt", "a")
    file = open ("data.txt", "r")
    leitura = (file.readline())

    
    # Verifica se há algum usuário cadastrado
    
    if leitura:
        
        exist_data = list (ast.literal_eval (str(leitura)))                      # Eval limpa o lixo resultante do readline. O resultado é transformado em lista
        exist_nome = exist_data [0]

    
        # Verificação de usuário existente
        
        if nome == exist_nome:

            # Se o usuário já é existente, faz a leitura dos dados gravados
            file = open ("data.txt", "r")
            exist_data = list (ast.literal_eval (str(leitura)))
            
            dia = exist_data [1]
            mes = exist_data [2]
            seu_signo = exist_data [3]
            signo_url = exist_data [4]
            
            print ('Olá %s,\nSeja bem vindo(a) de volta!' %nome)
            print ('Você faz aniversario no dia %s/%s' %(dia,mes))
            print ('Seu signo é %s' %seu_signo)


            # Opção para trocar os dados
            consulta = bool(int(input('\nPara ver a previsão do dia para seu signo, digite 0. \nOu digite 1 para alterar seus dados: ')))

            while consulta:
                cadastro (nome)
                consulta = bool(int(input('\nPara ver a previsão do dia para seu signo, digite 0. \nOu digite 1 para alterar seus dados: ')))

            previsao ()

            file.close


        else:
            # Caso contrário é feito o cadastro do novo usuário
            print ('Ola, %s. Seja bem vindo(a) ao Horóscopo. \nPara iniciarmos, precisamos saber seus dados.' %nome)       

            cadastro (nome)
            
            # Opção para trocar os dados
            consulta = bool(int(input('\nPara ver a previsão do dia para seu signo, digite 0. \nOu digite 1 para alterar seus dados: ')))

            while consulta:
                cadastro (nome)
                consulta = bool(int(input('\nPara ver a previsão do dia para seu signo, digite 0. \nOu digite 1 para alterar seus dados: ')))
 
            previsao ()


    else:
        # Não havendo nenhum dado gravado, é feito o cadastro de um novo usuário
        print ('Ola, %s. Seja bem vindo(a) ao Horóscopo. \nPara iniciarmos, precisamos saber seus dados.' %nome)
        
        cadastro (nome)

        # Opção para trocar os dados
        consulta = bool(int(input('\nPara ver a previsão do dia para seu signo, digite 0. \nOu digite 1 para alterar seus dados: ')))

        while consulta:
            cadastro (nome)
            consulta = bool(int(input('\nPara ver a previsão do dia para seu signo, digite 0. \nOu digite 1 para alterar seus dados: ')))
 
        previsao ()


# Função de cadastro de novo usuário
def cadastro(nome):
    
    # Novo usuário deve entrar com seus dados a partir daqui
    dia = int(input("Digite o dia do seu aniversário: "))

    while dia < 1 or dia > 31:
        print ("Dia digitado é inválido.")
        dia = int(input("Digite o dia do seu aniversário: "))

    mes = int(input("Digite o mês do seu aniversario: "))

    while mes < 1 or mes > 12:
        print ("Mês digitado é inválido")
        mes = int(input("Digite o mês do seu aniversario: "))
        
    user_data = [nome, dia, mes]

    # Dicionário - {mes : [data de troca, signo, nome sem acento]}
    signo = {1 : [20,'Aquário','aquario'],
             2 : [19,'Peixes','peixes'],
             3 : [21, 'Áries','aries'],
             4 : [20, 'Touro','touro'],
             5 : [21, 'Gêmeos','gemeos'],
             6 : [21, 'Câncer','cancer'],
             7 : [23, 'Leão','leao'],
             8 : [23, 'Virgem','virgem'],
             9 : [23, 'Libra','libra'],
            10 : [23, 'Escorpião','escorpiao'],
            11 : [22, 'Sagitário','sagitario'],
            12 : [22, 'Capricórnio','capricornio']}


    # Definição do signo de acordo com os valores inseridos pelo usuário
    lista = signo[mes]

    if mes == 1 and dia < lista[0]:
        mes = 12
        lista = signo[mes]
        seu_signo = lista[1]
        signo_url = lista[2]

    elif mes != 1 and dia < lista[0]:
        mes -= 1
        lista = signo[mes]
        seu_signo = lista[1]
        signo_url = lista[2]

    else:
        seu_signo = lista[1]
        signo_url = lista[2]

    # Informa ao usuário qual seu signo 
    print("Seu signo é %s " % seu_signo)

    # Grava os dados do usuário no arquivo txt para consulta futura
    file = open ("data.txt", "w")
    user_data += [seu_signo, signo_url]   
    file.write (str(user_data))
    file.close

    global signo_url
    return signo_url
    

# Busca previsão da web
def previsao ():

    global signo_url

    # Site IG
    link = urlopen("http://somostodosum.ig.com.br/horoscopo/signo/%s.html" %signo_url)
    previsao_ig = BeautifulSoup(link, "html.parser")
    previsao_ig_dia = previsao_ig.find ('p', {'class':'textogeral cinza'})

    print ('\nA previsão de hoje para seu signo (site IG - Somos todos um):\n') 
    print(previsao_ig_dia.text)


    # Site Extra
    link = urlopen("http://extra.globo.com/horoscopo/signo-de-%s/" %signo_url).read()
    previsao_extra = BeautifulSoup (link, "html.parser")
    previsao_extra_dia = previsao_extra.find ('div', {'class':'text-signo'})

    print ('\nA previsão de hoje para seu signo (site Extra):\n') 
    print(previsao_extra_dia.text)

    
main()

