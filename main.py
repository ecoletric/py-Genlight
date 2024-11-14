#Felipe Ribeiro Tardochi Da Silva Rm:555100
#Gustavo Dias da Silva Cruz Rm:556448
#Julia Medeiros Angelozi Rm:

import requests
import json

def estilizado(titulo):
    '''
    Essa função cria titulos estilizado mais facilmente.
    
    Parametro -> String (titulo)
    
    Printa o titulo estilizado
    '''
    x = len(titulo)
    y = round(x / 2)
    print(x * "---")
    print(y * "--" ,titulo, y * "--")
    print(x * "---")

def verificar_email(email):
    '''
    Essa função serve para verificar se o email e valido.
    
    Parametro -> String (Email)
    
    Retorna True caso o email tenha @.
    '''
    for x in email:
        if x == "@":
            return True
        

def verificar_informacoes(email, senha1, senha2, cnpj, cep):
    '''
    Essa função serve para verificar se as informações que a pessoa inputou estão certas.
    
    Parametro -> String (email, senha1, senha2, cpf, cep)
    
    Retorna True caso as informações estejam certas, e printa que o cadastro foi realizado, caso contrario retorna False e Printa que o cadastro não foi realizado.
    '''
    if verificar_email(email) and senha1 == senha2 and  len(cep) == 8 and len(cnpj) == 14:
        estilizado("Cadastro Realizado com sucesso")
        return True
    else:
        print("Você colocou informações erradas, cadastro não realizado.")
        return False
    

def cadastro():
    '''
    Essa função serve para pegar as informações do Usuário, e cadastra ele caso a função verificar informações retorne True.
    
    Parametro -> ()
    '''
    empresa = {}
    nome = input("Digite o seu nome: ")
    email = input("Digite o seu Email: ")
    senha = input("Digite a senha: ")
    senhaaux = input("Confirme a senha: ")
    cnpj = input("Digite o seu cpf: ")
    cep = input("Digite seu Cep(XXXXX-XXX): ")
    status = verificar_informacoes(email=email,senha1=senha,senha2=senhaaux, cnpj=cnpj, cep=cep)
    if status == True :
        id_enderecoaux = cadastrar_endereco(cep)
        id_endereco = int(id_enderecoaux['id_endereco'])
        if(id_endereco):
            user = cadastrar_empresa(nome=nome , senha=senha, cnpj=cnpj,email=email,empresa=empresa,id_endereco=id_endereco)
            return user
        else:
            print("Erro ao cadastrar pessoa")
            return
    else:
        estilizado("Não foi possível cadastrar a pessoa")
        return

def buscar_empresas():
    try:
        req = requests.get(f"http://127.0.0.1:5000/empresa")
        if req.status_code == 200:
            empresa = req.json()
            return empresa
        else:
            print("Nehuma empresa encontrada!")
            raise Exception("Erro ao buscar empresas")
    except Exception as e:
        print(e)

def login_empresa():
   
    empresas = buscar_empresas()

    
    cnpj_input = input("Digite o seu cnpj: ")
    senha_input = input("Digite a sua senha: ")


    for empresa in empresas:
        if empresa['cnpj'] == cnpj_input and empresa['senha'] == senha_input:
            print("Login realizado com sucesso!")
            print(f"Bem-vindo, {empresa['nome']}!")
            return empresa

   
    print("CPF ou senha incorretos.")
    return None
    
def cadastrar_empresa(nome,senha,cnpj,email,empresa,id_endereco):
    empresa["nome"] = str.capitalize(nome)
    empresa["senha"] = senha
    empresa["email"] = email
    empresa["cnpj"] = cnpj
    empresa['endereco'] = id_endereco

    user = requests.post("http://127.0.0.1:5000/empresa", json= empresa)
    if user.status_code == 200:
        user_json = user.json()
        return user_json
    else:
        print("Erro ao adicionar usuario")
    

def cadastrar_endereco(cep):
    try:
        endereco = buscar_cep(cep)
        if(endereco):
            res = requests.post("http://127.0.0.1:5000/endereco", json=endereco)
            if res.status_code == 200:
                id_endereco = res.json()
                return id_endereco
            else:
                print(f'Erro ao cadastrar endereço: {res.status_code} - {res.text}')
                raise Exception(f'Falha na requisição de cadastro: {res.status_code}')
        else:
            raise Exception('Falha ao buscar endereco')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
        raise

def buscar_cep(cep):
    tentativa = False
    try:
        while tentativa != True:
            url = f'https://viacep.com.br/ws/{cep}/json/'
            req = requests.get(url)
            dados = req.json()
            try:
                erro =False if dados['erro'] else True
            except:
                erro= True
            if req.status_code == 200 and erro:
                
                print(dados)
                endereco = {
                    'cep':cep,
                    'logradouro': dados['logradouro'],
                    'complemento': "Complemento insano",
                    'bairro': dados['bairro'],
                    'cidade': dados['localidade'],
                    'uf': dados['uf']
                }
                tentativa = True
                return endereco
            else:
                print(f'Erro ao buscar CEP: {req.status_code} - {req.text}')
                cep = input("Digite um novo cep")
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
        raise

def ler(lista):
    """    
    Essa função pergunta ao usuário se ele quer ler toda a lista ou ele quer ler uma unidade da lista.
    
    Parametro -> (lista)

    Return -> none
    """
    if lista:
        escolha = 0
        ler_escolha = False
        while not ler_escolha:
            escolha_bool = False
            while not escolha_bool:
                try:
                    escolha = int(input("Escolha entre as seguintes opções\n1)Ler unidade \n2)Ler todos os itens\n-1)sair\n"))
                    if escolha == 1 or escolha == 2 or escolha == -1:
                        escolha_bool= True
                    else:
                        print("Escolha uma opção valida!!")
                except ValueError:
                    print("Escolha uma opção valida!!")
            match escolha:
                case 1:
                    ler_escolha = ler_unidade(lista)
                case 2:
                    ler_escolha = ler_todos(lista)
                case -1:
                    estilizado("Saindo")
                    return
    else:
        print("Você ainda não tem nenhum registro!")

def ler_unidade(lista):
    """    
    Essa função serve para ler um index da lista que chegou na função.
    
    Parametro -> (lista)

    Return -> boolean
    """
    indice = len(lista)
    dic = lista[0]
    keys = list(dic.keys())
    text = ""
    for i in range(len(lista)):
        text += f"{i}){lista[i][keys[7]]}\n"

    escolha_bool = False
    while not escolha_bool:
        try:
            escolha = int(input(f"Escolha entre os carros \n{text}\n-1)sair\n"))
            if escolha == -1:
                return True
            elif escolha >= 0 and escolha < indice:
                escolha_bool= True
            else:
                print("Escolha uma opção valida!!")
        except ValueError: 
            print("Escolha uma opção valida!!")
    obj = lista[escolha]
    for x in obj.keys():
        print(f"{x} : {obj[x]}")
    return False

def ler_todos(lista):
    """    
    Essa função serve para ler todos os itens dentro de uma lista.
    
    Parametro -> (lista)
    """
    for i in range(len(lista)):
        obj = lista[i]
        for x in obj.keys():
            print(f"{x} : {obj[x]}")

def get_industrias(id_empresa):
    try:
        req = requests.get(f"http://127.0.0.1:5000/industria/listar/{id_empresa}")
        if req.status_code == 200:
            industrias = req.json()
            return industrias
        else:
            print("Nehum carro encontrado!")
            return []
    except Exception as e:
        print(e)

def crud_empresa(empresa):
    """    
    Essa função serve para realizar as informações possiveis com a lista de carros.
    
    Parametro -> (carros)

    """
    escolha = 0
    emp = empresa[0]
    id_empresa = emp['id_empresa']
    crud_escolha = False
    while not crud_escolha:
        lista_industrias = get_industrias(id_empresa)
        escolha_bool = False
        estilizado("Bem-vindo a central de seus veiculos")
        while not escolha_bool:
            try:
                escolha = int(input("Escolha entre as seguintes opções\n1)Inserir industrias\n2)Ver suas industrias\n3)Ataulizar informações da Empresa\n-1)sair\n"))
                if escolha == 1 or escolha == 2 or escolha ==3 or escolha==4 or escolha == -1:
                    escolha_bool= True
                else:
                    print("Escolha uma opção valida!!")
            except ValueError:
                print("Escolha uma opção valida!!")
        match escolha:
            case 1:
                crud_escolha = inserir_industria(lista_industrias,id_empresa)
            case 2:
                crud_escolha,industria= escolher_industria(lista_industrias)
                if(industria != None):
                    crud_industria(industria)
                else:
                    return
            case 3:
                crud_escolha = atualizar_empresa(emp)

            case -1:
                break
def crud_industria(industria):
    escolha = 0
    id_industria = industria['id_industria']
    crud_escolha = False
    while not crud_escolha:
        lista_sitios = get_sitios(id_industria)
        escolha_bool = False
        estilizado("Bem-vindo a central de seus veiculos")
        while not escolha_bool:
            try:
                escolha = int(input("Escolha entre as seguintes opções\n1)Inserir industrias\n2)Ver suas industrias\n-1)sair\n"))
                if escolha == 1 or escolha == 2 or escolha ==3 or escolha==4 or escolha == -1:
                    escolha_bool= True
                else:
                    print("Escolha uma opção valida!!")
            except ValueError:
                print("Escolha uma opção valida!!")
        match escolha:
            case 1:
                crud_escolha = cadastrar_sitio(lista_sitios,id_industria)
            case 2:
                crud_escolha,sitio= escolher_industria(lista_sitios)
                if(sitio != None):
                    crud_sitio(sitio)
                else:
                    return
            case -1:
                break

def crud_sitio(sitio):
    escolha = 0
    tp_sitio = sitio['tp_sitio']
    lista = []
    id_sitio = sitio['id_industria']
    crud_escolha = False
    while not crud_escolha:
        if tp_sitio == 0:
            lista = get_maquinas(id_sitio)
        elif tp_sitio == 1 or tp_sitio == 2:
            lista = get_fonte(id_sitio)
        escolha_bool = False
        estilizado("Bem-vindo a do sitio de seus veiculos")
        while not escolha_bool:
            try:
                escolha = int(input("Escolha entre as seguintes opções\n1)Cadastrar fonte\n2)Informações do sitio\n-1)sair\n"))
                if escolha == 1 or escolha == 2 or escolha == -1:
                    escolha_bool= True
                else:
                    print("Escolha uma opção valida!!")
            except ValueError:
                print("Escolha uma opção valida!!")
        match escolha:
            case 1:
                if tp_sitio == 0:
                    crud_escolha = cadastrar_maquina(id_sitio,lista)
                elif tp_sitio == 1 or tp_sitio == 2:
                    crud_escolha = cadastrar_fonte(id_sitio,lista)
            case 2:
                crud_escolha = informacoes_sitio(tp_sitio,lista,sitio)
            case -1:
                break

def informacoes_sitio(tp_sitio,lista,sitio):
    estilizado("Bem vindo as informações do sitio")
    tipo = "Maquina" if tp_sitio == 0 else "Solar" if tp_sitio == 1 else "Eolico"
    consumo = calcular_consumo(lista)
    id_endereco = sitio['id_endereco']
    endereco = get_endereco(id_endereco)
    print(f"""
        Tipo:{tipo}
        Consumo/Potencia:{consumo}
        Cep:{endereco['cep']}
        Logradouro:{endereco['logradouro']}
        Estado:{endereco['uf']}
    """)

def get_endereco(id_endereco):
    try:
        req = requests.get(f"http://127.0.0.1:5000/endereco/{id_endereco}")
        if req.status_code == 200:
            endereco = req.json()
            return endereco
        else:
            print("Nehum endereco encontrado!")
            return []
    except Exception as e:
        print(e)

def calcular_consumo(lista):
    consumo = 0
    for item in lista:
        consumo += item['consumo']
    return consumo


def cadastrar_fonte(id_sitio,lista):
    print("Bem vindo ao sessão de cadastro de fontes!")
    tentativa = False
    while tentativa != True:
        try:
            tentativa = False
            potencia = 0
            while tentativa !=True:
                try:
                    potencia = int(input("Qual a potencia da fonte: "))
                    quantidade = int(input("Digite a quantidade de fontes"))
                    tipo = int(input("Escolha o tipo da fonte\n[1] Solar. \n[2] Eólica.\n"))
                    if(1<=tipo>=2):
                        tentativa = True
                except:
                    print("Escreva uma opção valida!")
            for _ in range(quantidade):
                fonte = adicionar_fonte(tipo=tipo,potencia=potencia,id_sitio=id_sitio)
                if(fonte):
                    lista.append(fonte)
            if(fonte):   
                print("Fonte(s) adicionada(s) com sucesso!")
                return fonte
            else:
                print("Falha ao adicionar sitio")
                return
        except ValueError:
            print("Falha adicionar valor, tente novamente!")

def adicionar_fonte(tipo,potencia,id_sitio):
    fonte = {}
    fonte['potencia'] = potencia
    fonte['tipo'] = tipo
    fonte['id_sitio'] = id_sitio
    req = requests.post("http://127.0.0.1:5000/aparelhoGerado",json=fonte)
    if req.status_code == 200:
        return fonte
    else:
        print("Erro ao adicionar maquina")
        return None

def cadastrar_maquina(id_sitio,lista):
    print("Bem vindo ao sessão de cadastro de maquinas!")
    tentativa = False
    while tentativa != True:
        try:
            tentativa = False
            consumo = 0
            while tentativa !=True:
                try:
                    consumo = int(input("Qual o consumo da maquina: "))
                    quantidade = int(input("Digite a quantidade de maquinas"))
                    tentativa= True
                except:
                    print("Escreva uma opção valida!")
            descricao = input("Descrição da maquina: ")
            for _ in range(quantidade):
                maquina = adicionar_maquina(descricao=descricao,potencia=consumo,id_sitio=id_sitio)
                if(maquina):
                    lista.append(maquina)
            if(maquina):   
                print("Maquina(s) adicionada(s) com sucesso!")
                return maquina
            else:
                print("Falha ao adicionar sitio")
                return
        except ValueError:
            print("Falha adicionar valor, tente novamente!")


def adicionar_maquina(descricao,potencia,id_sitio):
    maquina = {}
    maquina['consumo'] = potencia
    maquina['ds_maquina'] = descricao
    maquina['id_sitio'] = id_sitio
    req = requests.post("http://127.0.0.1:5000/maquina",json=maquina)
    if req.status_code == 200:
        return maquina
    else:
        print("Erro ao adicionar maquina")
        return None

def get_maquinas(id_sitio):
    try:
        req = requests.get(f"http://127.0.0.1:5000/maquina/listar/{id_sitio}")
        if req.status_code == 200:
            maquinas = req.json()
            return maquinas
        else:
            print("Nehuma maquina encontrada!")
            return []
    except Exception as e:
        print(e)

def get_fonte(id_sitio):
    try:
        req = requests.get(f"http://127.0.0.1:5000/aparelhoGerado/listar/{id_sitio}")
        if req.status_code == 200:
            fonte = req.json()
            return fonte
        else:
            print("Nehum carro encontrado!")
            return []
    except Exception as e:
        print(e)

def get_sitios(id_industria):

    try:
        req = requests.get(f"http://127.0.0.1:5000/sitios/listar/{id_industria}")
        if req.status_code == 200:
            sitios = req.json()
            return sitios
        else:
            print("Nehum carro encontrado!")
            return []
    except Exception as e:
        print(e)

def cadastrar_sitio(lista_sitios,id_industria):
    print("Bem vindo ao sessão de cadastro de sitios!")
    tentativa = False
    while tentativa != True:
        try:
            tentativa = False
            tp_sitio = 0
            while tentativa !=True:
                try:
                    tp_sitio = int(input("Escolha o tipo do sitio\n[0] Consumo(Máquinas).\n[1] Solar. \n[2] Eólica.\n"))
                    if 0<= tp_sitio <=2 :
                        tentativa= True
                    else:
                        print("Escreva uma opção valida!")
                except:
                        print("Escreva uma opção valida!")
            cep = input("Qual o cep do sitio?\n")
            endereco = cadastrar_endereco(cep)
            sitio = adicionar_sitio(endereco,id_industria,tp_sitio)
            if(sitio):   
                print("Sitio adicionado com sucesso!")
                lista_sitios.append(sitio)
                return sitio
            else:
                print("Falha ao adicionar sitio")
                return
        except ValueError:
            print("Falha adicionar valor, tente novamente!")

def adicionar_sitio(endereco,id_industria,tp_sitio):
    sitio = {}
    id_endereco = endereco['id_endereco']
    sitio['id_endereco'] = id_endereco
    sitio['tp_sitio'] = tp_sitio
    sitio['id_industria'] = id_industria
    req = requests.post("http://127.0.0.1:5000/industria",json=sitio)
    if req.status_code == 200:
        return sitio
    else:
        print("Erro ao adicionar carro")
        return None

def escolher_industria(industrias):
    indice = len(industrias)
    dic = industrias[0]
    keys = list(dic.keys())
    text = ""
    for i in range(indice):
        text += f"{i}){industrias[i][keys[1]]}\n"
        escolha_bool = False
    while not escolha_bool:
        try:
            escolha = int(input(f"Escolha entre os indice \n{text}\n-1)sair\n"))
            if escolha == -1:
                return True, None
            elif escolha >= 0 and escolha < indice:
                escolha_bool= True
                return True,industrias[escolha]
            else:
                print("Escolha uma opção valida!!")
                return False,None
        except ValueError: 
            print("Escolha uma opção valida!!")

def cadastrar_industria(id_empresa):
    print("Bem vindo ao sessão de cadastro de industria!")
    tentativa = False
    while tentativa != True:
        nome = input("Qual o nome da industria?\n")
        industria = adicionar_industria(nome,id_empresa=id_empresa)
        if(industria):   
            print("Industria adicionada com sucesso!")
            return industria
        else:
            return

def adicionar_industria(nome,id_empresa):
    industria = {}
    industria['nome'] = nome
    industria['id_empresa'] = id_empresa
    req = requests.post("http://127.0.0.1:5000/industria",json=industria)
    if req.status_code == 200:
        return industria
    else:
        print("Erro ao adicionar carro")
        return None
def atualizar_empresa(lista):
    """    
    Essa função serve para atualizar uma chave de um dicionario dentro da lista que chega na função.
    
    Parametro -> (lista)

    Return -> none
    """
    if lista:
        indice = 0
        dic = lista[0]
        keys = [list(dic.keys())]
        
        text_2 = ""
        for i in range(len(lista)):
            text_2 += f"{i}){lista[i][keys[0][1]]}\n"
        escolha_bool = False
        while not escolha_bool:
            try:
                indice = int(input(f"Escolha algum dos seguintes indices:  \n{text_2}\n-1)sair\n"))
                if indice == -1:
                    return
                elif indice >= 0 and indice < len(lista):
                    escolha_bool = True
                else:
                    print("Escolha uma opção valida!!")
            except ValueError: 
                print("Escolha uma opção valida!!")
        empresa = lista[indice]
        id_empresa = empresa['id_empresa']
        nome_valido = False
        while nome_valido != True:
            try:
                email = input("Digite o novo email: \n")
                senha = input("Digite a nova senha: ")
                senha_aux = input("Digite a nova senha: ")
                if verificar_email(email) and senha == senha_aux:
                    nome_valido=True
                else:
                    print("Email invalido ou senhas diferentes!!")
            except ValueError:
                print("Você precisa inserir um numero!") 
        empresa_dict = {
            'email':email,
            'senha':senha
        }

        req = requests.put(f"http://127.0.0.1:5000/empresa/{id_empresa}",json=empresa_dict)
        if req.status_code == 200:
            print("Informações atualizadas com sucesso")
        else:
            print("Falha ao atualizar informações")
    else:
        print("Você não possui nenhum item para atualizar ainda.")

def inserir_industria(lista,id_empresa):
    """    
    Essa função insere o carro na lista de carros.
    
    Parametro -> (lista,id_usuario) - lista de carros

    """
    industria = cadastrar_industria(id_empresa)
    if industria != None:
        lista.append(industria)
        print("Industria Adicionada")
    else:
        return



def menu():
    """    
    Essa função mostrar o menu para o usuario.
    
    Parametro -> ()

    Return -> opcao_saida (escolha)
    """
    tentativa = False
    while tentativa !=True:
        try:
            opcao_saida = int(input("Olá tudo bem, qual seria sua necessidade.\n[1] logar-se.\n[2] Cadastrar-se. \n[3] Industrias. \n[4] Informações.\n[5] Json(s).\n[-1] Para sair.\n"))
            if 0< opcao_saida <=8 or opcao_saida == -1:
                tentativa= True
                return opcao_saida
            else:
                print("Escreva uma opção valida!")
        except:
                print("Escreva uma opção valida!")

def decisao(opcao,empresa):
    """    
    Essa função serve para chamar a função de acordo com a decisão tomada pelo usuário na função de menu.
    
    Parametro -> (ocorrencias,problema,carro,link)

    """
    if opcao <= 8 and opcao > 0  or opcao == -1:
        match opcao:
            case 1:
                if not empresa: 
                    user = login_empresa()
                    empresa.append(user)
                else:
                    print("Você ja esta logado!")
            case 2:
                if not empresa:
                    user = cadastro()
                    if user != None:
                        print(user)
                        empresa.append(user)
                else:
                    print("Você ja esta logado!")
            case 3:
                if empresa:
                    emp = empresa[0]
                    id_empresa = empresa['id_empresa']
                    crud_empresa(emp,id_empresa=id_empresa)
                else:
                    print("Você não está logado!")
            case 4:
                if empresa:
                    emp = empresa[0]
                    id_empresa = empresa['id_empresa']
                    crud(emp,id_empresa=id_empresa)
                else:
                    print("Você não está logado!")
            case 5:
                escolha = exportar_json()
                exportar_escolha(escolha)
            case -1:
                estilizado("Obrigado, volte sempre!")
    else:
        print("So aceitamos numeros de 1 à 4 ou -1\nDIGITE UM VALOR VÁLIDO!!! ")



def main():
    empresa = []
    opcao_saida = 0
    while opcao_saida != -1:
        opcao_saida = menu()
        decisao(opcao_saida,empresa)