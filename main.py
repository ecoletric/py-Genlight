#Felipe Ribeiro Tardochi Da Silva Rm:555100
#Gustavo Dias da Silva Cruz Rm:556448
#Julia Medeiros Angelozi Rm: 556364

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
    nome = input("Digite o nome da empresa: ")
    email = input("Digite o email para contato: ")
    senha = input("Digite a senha: ")
    senhaaux = input("Confirme a senha: ")
    cnpj = input("Digite o seu cnpj: ")
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
            print(f"Bem-vindo, {empresa['nome_empresa']}!")
            return empresa

   
    print("Cnpj ou senha incorretos.")
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
                
                endereco = {
                    'cep':cep,
                    'logradouro': dados['logradouro'],
                    'complemento': "Complemento insano",
                    'bairro': dados['bairro'],
                    'cidade': dados['localidade'],
                    'uf': dados['uf']
                }
                tentativa = True
                print(endereco)
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
            print("Nehuma industria encontrado!")
            return []
    except Exception as e:
        print(e)

def crud_empresa(empresa):
    """    
    Essa função serve para realizar as informações possiveis com a lista de carros.
    
    Parametro -> (carros)

    """
    escolha = 0
    id_empresa = empresa['id_empresa']
    crud_escolha = False
    while not crud_escolha:
        lista_industrias = get_industrias(id_empresa)
        escolha_bool = False
        estilizado("Bem-vindo a central de informações da empresa")
        while not escolha_bool:
            try:
                escolha = int(input("Escolha entre as seguintes opções\n1)Inserir industrias\n2)Ver suas industrias\n3)Atualizar informações da Empresa\n4)Informações empresa \n-1)sair\n"))
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
                crud_escolha = atualizar_empresa(empresa)
            case 4:
                crud_escolha = informacoes_empresa(empresa)
            case -1:
                break


def informacoes_empresa(empresa):
    estilizado("Bem vindo as informações da Empresa")
    id_endereco = empresa['id_endereco']
    id_empresa = empresa['id_empresa']
    emp = get_empresa(id_empresa)
    endereco = get_endereco(id_endereco)
    print(f"""
        Nome:{emp['nome_empresa']}
        Email:{emp['email']}
        Senha:{emp['senha']}
        Cnpj:{emp['cnpj']}
        Cep:{endereco['cep']}
        Logradouro:{endereco['logradouro']}
        Estado:{endereco['uf']}
    """)

def get_empresa(id_empresa):
    try:
        req = requests.get(f"http://127.0.0.1:5000/empresa/{id_empresa}")
        if req.status_code == 200:
            empresa = req.json()
            return empresa
        else:
            print("Nehuma industria encontrado!")
            return []
    except Exception as e:
        print(e)


def crud_industria(industria):
    escolha = 0
    id_industria = industria['id_industria']
    crud_escolha = False
    while not crud_escolha:
        lista_sitios = get_sitios(id_industria)
        escolha_bool = False
        estilizado(f"Bem-vindo a central de infomações da sua industria: {industria['nm_industria']}")
        while not escolha_bool:
            try:
                escolha = int(input("Escolha entre as seguintes opções\n1)Inserir sitio\n2)Ver seus sitios\n3)Ver Informação da Industria\n-1)sair\n"))
                if escolha == 1 or escolha == 2 or escolha == 3 or escolha == -1:
                    escolha_bool= True
                else:
                    print("Escolha uma opção valida!!")
            except ValueError:
                print("Escolha uma opção valida!!")
        match escolha:
            case 1:
                crud_escolha = cadastrar_sitio(lista_sitios,id_industria)
            case 2:
                if lista_sitios:
                    crud_escolha,sitio= escolher_industria(lista_sitios)
                    if(sitio != None):
                        crud_escolha = crud_sitio(sitio)
                    else:
                        return True
                else:
                    print("Você não tem nenhum sitio cadastrado para essa industria")
            case 3:
                crud_escolha = informacoes_industria(industria)
            case -1:
                break

def informacoes_industria(industria):
    estilizado("Bem vindo as informações da Industria")
    print("Caso o valor seja negativo é porque a industria está com deficit energia")
    print("Adicione fontes de energia para suprir a demanda")
    print(f"""
        Nome:{industria['nm_industria']}
        Geração:{calcular_geracao(industria['id_industria'])}KW
    """)
    return False

def calcular_geracao(id_industria):
    try:
        sitios = get_sitios(id_industria)
        geracao = 0
        consumo = 0
        for sitio in sitios:
            tp_sitio = sitio['tp_fonte']
            if tp_sitio == 0:
                maquinas = get_maquinas(sitio['id_sitio'])
                consumo += calcular_consumo(maquinas)
            elif tp_sitio == 1 or tp_sitio == 2:
                fontes = get_fonte(sitio['id_sitio'])
                consumo += calcular_consumo(fontes)
            geracao += consumo
        return geracao 
    except:
        print("Erro ao calcular geração")

def crud_sitio(sitio):
    escolha = 0
    tp_sitio = sitio['tp_fonte']
    lista = []
    id_sitio = sitio['id_sitio']
    crud_escolha = False
    while not crud_escolha:
        if tp_sitio == 0:
            lista = get_maquinas(id_sitio)
        elif tp_sitio == 1 or tp_sitio == 2:
            lista = get_fonte(id_sitio)
        escolha_bool = False
        estilizado("Bem-vindo a central de informações do sitio")
        while not escolha_bool:
            try:
                escolha = int(input("Escolha entre as seguintes opções\n1)Cadastrar fonte\n2)Informações do sitio\n3)Excluir fonte\n-1)sair\n"))
                if escolha == 1 or escolha == 2 or escolha == 3 or escolha == -1:
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
                    crud_escolha = cadastrar_fonte(id_sitio,lista,tp_sitio)
            case 2:
                crud_escolha = informacoes_sitio(tp_sitio,lista,sitio)
            case 3:
                if tp_sitio == 0:
                    crud_escolha = excluir_maquina(lista)
                elif tp_sitio == 1 or tp_sitio == 2:
                    crud_escolha = excluir_fonte(lista)
            case -1:
                break

def excluir_maquina(lista):
    """    
    Essa função serve pra excluir um item pelo indice que ele está na lista.
    
    Parametro -> (lista)
    """
    if lista:
        indice = 0
        dic = lista[0]
        escolha = 0
        keys = list(dic.keys())
        text = ""
        for i in range(len(lista)):
            text += f"{i}){lista[i][keys[0]]}\n"
        escolha_bool = False
        while not escolha_bool:
            try:
                indice = int(input(f"Escolha algum dos seguintes indices para excluir:  \n{text}-1)sair\n"))
                if indice == -1:
                    return
                elif indice >= 0 and indice < len(lista):
                    escolha_bool = True
                else:
                    print("Escolha uma opção valida!!")
            except ValueError: 
                print("Escolha uma opção valida!!")
        escolha_bool = False
        maquina = lista[indice]
        id_maquina = maquina['id_maquina']
        while not escolha_bool:
            try:
                escolha = int(input(f"Você tem certeza que deseja excluir esse registro (Ação irreverssivel):  \n1)Sim\n2)Não\n-1)sair\n"))
                if escolha == 1 or escolha == 2:
                    escolha_bool = True
                else:
                    print("Escolha uma opção valida!!")
            except ValueError: 
                print("Escolha uma opção valida!!")
        match escolha:
            case 1:
                req = requests.delete(f"http://127.0.0.1:5000/maquina/{id_maquina}")
                if req.status_code == 200:
                    print("Item excluido com sucesso")
                    return
                else:
                    print("Falha ao excluir maquina")
                    return
            case 2:
                return
    else:
        print("Você não tem nenhum registro ainda pra excluir!")

def excluir_fonte(lista):
    """    
    Essa função serve pra excluir um item pelo indice que ele está na lista.
    
    Parametro -> (lista)
    """
    if lista:
        indice = 0
        dic = lista[0]
        escolha = 0
        keys = list(dic.keys())
        text = ""
        for i in range(len(lista)):
            text += f"{i}){lista[i][keys[0]]}\n"
        escolha_bool = False
        while not escolha_bool:
            try:
                indice = int(input(f"Escolha algum dos seguintes indices para excluir:  \n{text}-1)sair\n"))
                if indice == -1:
                    return
                elif indice >= 0 and indice < len(lista):
                    escolha_bool = True
                else:
                    print("Escolha uma opção valida!!")
            except ValueError: 
                print("Escolha uma opção valida!!")
        escolha_bool = False
        carro = lista[indice]
        id_fonte = carro['id_fonte']
        while not escolha_bool:
            try:
                escolha = int(input(f"Você tem certeza que deseja excluir esse registro (Ação irreverssivel):  \n1)Sim\n2)Não\n-1)sair\n"))
                if escolha == 1 or escolha == 2:
                    escolha_bool = True
                else:
                    print("Escolha uma opção valida!!")
            except ValueError: 
                print("Escolha uma opção valida!!")
        match escolha:
            case 1:
                req = requests.delete(f"http://127.0.0.1:5000/aparelhoGerado/{id_fonte}")
                if req.status_code == 200:
                    print("Item excluido com sucesso")
                    return
                else:
                    print("Falha ao excluir aparelho gerador")
                    return
            case 2:
                return
    else:
        print("Você não tem nenhum registro ainda pra excluir!")


def informacoes_sitio(tp_sitio,lista,sitio):
    estilizado("Bem vindo as informações do sitio")
    tipo = "Maquina" if tp_sitio == 0 else "Solar" if tp_sitio == 1 else "Eolico"
    consumo = calcular_consumo(lista)
    id_endereco = sitio['id_endereco']
    endereco = get_endereco(id_endereco)
    print(f"""
        Tipo:{tipo}
        Consumo/Potencia:{consumo} KW
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
        consumo += item['consumo'if 'consumo' in item else 'potencia']
    return consumo



def cadastrar_fonte(id_sitio,lista, tp_sitio):
    print("Bem vindo ao sessão de cadastro de fontes!")
    tentativa = False
    while tentativa != True:
        try:
            tentativa = False
            potencia = 0
            while tentativa !=True:
                try:
                    potencia = int(input("Qual a potencia da fonte: "))
                    quantidade = int(input("Digite a quantidade de fontes: "))
                    if potencia > 0 and quantidade > 0:
                        tentativa= True
                        break
                except:
                    print("Escreva uma opção valida!")
            for _ in range(quantidade):
                fonte = adicionar_fonte(tipo=tp_sitio,potencia=potencia,id_sitio=id_sitio)
                if(fonte):
                    lista.append(fonte)
            if(fonte):   
                print("Fonte(s) adicionada(s) com sucesso!")
                return False
            else:
                print("Falha ao adicionar sitio")
                return True
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
                    quantidade = int(input("Digite a quantidade de maquinas: "))
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
                return False
            else:
                print("Falha ao adicionar sitio")
                return True
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
    except:
        print("Erro ao exportar dados")

def get_fonte(id_sitio):
    try:
        req = requests.get(f"http://127.0.0.1:5000/aparelhoGerado/listar/{id_sitio}")
        if req.status_code == 200:
            fonte = req.json()
            return fonte
        else:
            print("Nehuma fonte encontrado!")
            return []
    except:
        print("Erro ao exportar dados")

def get_sitios(id_industria):

    try:
        req = requests.get(f"http://127.0.0.1:5000/sitio/listar/{id_industria}")
        if req.status_code == 200:
            sitios = req.json()
            return sitios
        else:
            print("Nehum sitio encontrado!")
            return []
    except:
        print("Erro ao exportar dados")

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
                return False
            else:
                print("Falha ao adicionar sitio")
                return True
        except ValueError:
            print("Falha adicionar valor, tente novamente!")

def adicionar_sitio(endereco,id_industria,tp_sitio):
    sitio = {}
    id_endereco = endereco['id_endereco']
    sitio['id_endereco'] = id_endereco
    sitio['tp_sitio'] = tp_sitio
    sitio['id_industria'] = id_industria
    req = requests.post("http://127.0.0.1:5000/sitio",json=sitio)
    if req.status_code == 200:
        return sitio
    else:
        print("Erro ao adicionar sitio")
        return None

def escolher_industria(industrias):
    indice = len(industrias)
    dic = industrias[0]
    keys = list(dic.keys())
    text = ""
    for i in range(indice):
        text += f"{i}){industrias[i][keys[2]]}\n"
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
        escolha_bool = False
        while not escolha_bool:
            try:
                indice = int(input(f"Escolha qual informação você deseja atualizar \n1)Email\n2)Senha\n-1)sair\n"))
                if indice == -1:
                    return
                elif indice > 0 and indice <= 2:
                    escolha_bool = True
                else:
                    print("Escolha uma opção valida!!")
            except ValueError: 
                print("Escolha uma opção valida!!")
        id_empresa = lista['id_empresa']
        nome_valido = False
        tentativa = False
        senha = ''
        email = ''
        while nome_valido != True:
            try:
                if indice == 1:
                    email = input("Digite o novo email: \n")
                    if verificar_email(email) and email != lista['email'] and email != '':
                        tentativa = True
                elif indice == 2:
                    senha = input("Digite a nova senha: ")
                    senha_aux = input("Digite a nova senha: ")
                    if senha == senha_aux and senha != '' and senha_aux != '':
                        tentativa = True
                if tentativa:
                    nome_valido=True
                else:
                    print("Email invalido ou senhas diferentes!!")
            except ValueError:
                print("Você precisa inserir um numero!") 
        empresa_dict = {
            'email':email if email else lista['email'],
            'senha':senha if senha else lista['senha']
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
            opcao_saida = int(input("Olá tudo bem, qual seria sua necessidade.\n[1] logar-se.\n[2] Cadastrar-se. \n[3] Empresa.\n[4] Json(s).\n[-1] Para sair.\n"))
            if 0< opcao_saida <=8 or opcao_saida == -1:
                tentativa= True
                return opcao_saida
            else:
                print("Escreva uma opção valida!")
        except:
                print("Escreva uma opção valida!")

def exportar_json():
    tentativa = False
    while tentativa !=True:
        try:
            opcao_saida = int(input("Escolha qual tabela você quer extrair para JSON: \n[1] Industrias por empresa.\n[2] Sitios por industria.\n[3] Maquinas por sitio.\n[4] Geradores por sitio.\n[-1] Para sair.\n"))
            if 0< opcao_saida <=6 or opcao_saida == -1:
                tentativa= True
                return opcao_saida
            else:
                print("Escreva uma opção valida!")
        except:
                print("Escreva uma opção valida!")

def exportar_escolha(escolha,empresa,industrias,sitios,maquinas,fontes):
        match escolha:
            case 1:
                (boolean,industria) = escolher_industria(industrias=industrias)
                if industria != None:
                    with open('industrias.json', 'w') as f:
                        json.dump(industria, f, indent=4)
                        print("Industria exportada com sucesso")
                else:
                    print("Não foi possível exportar a tabela industria.")
            case 2:
                (boolean,sitio) = escolher_industria(industrias=sitios)
                if sitio != None:
                    with open('sitios.json', 'w') as f:
                        json.dump(sitio, f, indent=4)
                        print("Sitio exportado com sucesso")
                else:
                    print("Não foi possível exportar a tabela sitio.")
            case 3:
                (boolean,maquina) = escolher_industria(industrias=maquinas)
                if maquina != None:
                    with open('maquinas.json', 'w') as f:
                        json.dump(maquina, f, indent=4)
                        print("Maquina exportada com sucesso")
                else:
                    print("Não foi possível exportar a tabela maquina.")
            case 4:
                (boolean,fonte) = escolher_industria(industrias=fontes)
                if fonte != None:
                    with open('fontes.json', 'w') as f:
                        json.dump(fonte, f, indent=4)
                        print("Fonte exportada com sucesso")
                else:
                    print("Não foi possível exportar a tabela fonte.")
            case -1:
                estilizado("saindo")
                return

def decisao(opcao,empresa):
    """    
    Essa função serve para chamar a função de acordo com a decisão tomada pelo usuário na função de menu.
    
    Parametro -> (ocorrencias,problema,carro,link)

    """
    if opcao <= 8 and opcao > 0  or opcao == -1:
        match opcao:
            case 1:
                if not empresa or empresa == None: 
                    user = login_empresa()
                    empresa.append(user)
                else:
                    print("Você ja esta logado!")
            case 2:
                if not empresa or empresa == None:
                    user = cadastro()
                    if user != None:
                        empresa.append(user)
                else:
                    print("Você ja esta logado!")
            case 3:
                if empresa or empresa == None:
                    emp = empresa[0]
                    id_empresa = emp['id_empresa']
                    crud_empresa(emp)
                else:
                    print("Você não está logado!")
            case 4:
                if  empresa or empresa != None: 
                    emp = empresa[0]
                    industrias = get_industrias(emp['id_empresa'])
                    sitios =  []
                    for industria in industrias:
                        id_industria = industria['id_industria']
                        sitioss = get_sitios(id_industria)
                        for sitio in sitioss:
                            sitios.append(sitio)
                    maquinas = []
                    for sitio in sitios:
                        maquina = get_maquinas(sitio['id_sitio'])
                        for m in maquina:
                            maquinas.append(m)
                    fontes = []
                    for sitio in sitios:
                        fonte = get_fonte(sitio['id_sitio'])
                        for f in fonte:
                            fontes.append(f)
                    escolha = exportar_json()
                    exportar_escolha(escolha,emp,industrias,sitios,maquinas,fontes)
                else:
                    print("Você não está logado!")
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


#--------------------------------------------------------------principal-------------------------------------------------------------------------------------
main()