# coding=utf-8
import models
from models import *
from functions import *
models.init()

##########################################################################
# Função disponibilizada no WS para validar e importar a malha fornecida #
##########################################################################
def geraMalha(inputMapa, inputMalha):
    # lendo e ordenando linhas da malha
    linhas = inputMalha.strip().splitlines()
    linhas.sort()
    # criando listas que servirão para controle dos testes e geração das rotas
    ref = []
    lines = []
    rs = []
    foraPadrao = []
    valorNaoNumerico = []
    duplicidades = []
    ciclicos = []
    erros = False
    # realizando testes de verificação da malha e armazenando linhas válidas
    for linha in linhas:
        itens = linha.strip().split()
        # teste de formatação da linha
        if (len(itens) != 3):
            erros = True
            foraPadrao.append(linha)
        start = itens[0]
        end = itens[1]
        dist = itens[2]
        # verificando se a distância fornecida é um valor numérico
        if (not is_number(dist)):
            erros = True
            valorNaoNumerico.append(linha)
        # verificando existência de duplicidades
        if start+" "+end in rs:
            erros = True
            duplicidades.append(linhas[rs.index(start+" "+end)]+" - "+linha)
        # verificando existência de referências cíclicas
        if end+" "+start in rs:
            erros = True
            ciclicos.append(linhas[rs.index(end+" "+start)]+" - "+linha)

        rs.append(start+" "+end)
        lines.append(linha.strip())
        ref.append(start)

    # Verificando a existência de erros e, em caso positivo, preparando a mensagem de retorno para o cliente
	# Foram utilizados tags e códigos HTML nas mensgens para facilitar sua vilualização no navegador
    if erros:
        mensagemErro = ""
        if len(foraPadrao) > 0:
            mensagemErro += u"Existe(m) linha(s) na malha que não está(ão) no formato esperado: 'origem destino distância':<br />"
            mensagemErro += u"<br />".join(foraPadrao)+"<br /><br />"
        if len(valorNaoNumerico) > 0:
            mensagemErro += u"Existem rotas em que a distância não está em formato numérico:<br />"
            mensagemErro += u"<br />".join(valorNaoNumerico)+"<br /><br />"
        if len(duplicidades) > 0:
            mensagemErro += u"Existem rotas com pontos de origem e destino duplicados na malha fornecida:<br />"
            mensagemErro += u"<br />".join(duplicidades)+"<br /><br />"
        if len(ciclicos) > 0:
            mensagemErro += u"Foram encontradas referências cíclicas na malha fornecida:<br />"
            mensagemErro += u"<br />".join(ciclicos)+"<br /><br />"
        mensagemErro += u"A malha não foi importada.".encode("ascii", "xmlcharrefreplace")
        return {"status": 1, "message": mensagemErro.encode("ascii", "xmlcharrefreplace")}

    # carregando ou criando mapa
    if (inputMapa['id'] == 0):
        # criando novo mapa
        mapa = Mapa(nome_mapa=inputMapa['nome'])
        mapa.save()
    else:
        # carregando mapa existente
        mapa = Mapa(id=inputMapa["id"], nome_mapa=inputMapa["nome"])
        # excluindo rotas antigas pertencentes à esse mapa
        q = Rota.delete().where(Rota.mapa == mapa)
        q.execute()

    #criando dicionário que armazenará as rotas
    arrRes = dict()
    # para cada linha da malha fornecida, buscaremos as rotas sequentes possíveis
    # Ex. malha:
    # A B 10
    # B C 5
    # C D 20
    #
    # Rotas resultantes:
    # A B 10
    # A B C 15
    # A B C D 35
    # B C 5
    # B C D 25
    # C D 20
    for line in lines:
        itens = line.split()
        inicio = itens[0]
        buscaRota(lines, ref, inicio, 0, arrRes)

    # criando um dicionário que será utilizado na inserção massiva
    data_source = []
    for nome in arrRes:
        data_source.append({
            'nome_rota' : nome,
            'inicio' : arrRes[nome]["inicio"],
            'fim' : arrRes[nome]["fim"],
            'distancia' : arrRes[nome]["dist"],
            'mapa' : mapa
        })

    # insert massivo no BD para otimização. Inserindo 1000 linhas por vez.
    with db.atomic():
        for idx in range(0, len(data_source), 1000):
            Rota.insert_many(data_source[idx:idx+1000]).execute()

    # em caso de sucesso, mensagem de retorno
    return {"status": 0, "message": "Malha importada com sucesso!"}

###############################################################
# Função que checa a existência de um mapa com nome fornecido #
###############################################################
def checaMapa(mapa):
    # buscando mapa com o nome fornecido
    mapasDB = Mapa.filter(nome_mapa = mapa)
    # caso o mapa não exista, informar para o cliente id = 0
    if (len(mapasDB) == 0):
        return {"status": 0, "message": "Novo Mapa", "mapa": {"id": 0, "nome": mapa}}
    # caso o mapa exista, informar o id do mapa
    else:
        mapa = mapasDB[0]
        return {"status": 1, "message": "Mapa Existente", "mapa": {"id": mapa.id, "nome": mapa.nome_mapa}}

##############################################################
# Função que busca a menor rota com os parâmetros fornecidos #
##############################################################
def consultaRota(inputMapa, origem, destino, autonomia, valor_litro):
    # verificar a existência do mapa com o nome fornecido
    mapasDB = Mapa.filter(nome_mapa = inputMapa)
    if (len(mapasDB) == 0):
        # caso o mapa não exista, interromper o processo e informar ao cliente
        return {"status": 1, "message": u"Mapa não encontrado".encode("ascii", "xmlcharrefreplace")}
    else:
        # caso o mapa exista, vamos utilizá-lo adiante
        mapa = mapasDB[0]

    # Query para buscar as rotas que pertençam ao mapa fornecido 
    # e que satisfaçam os parâmetros de origem e destino.
    # Como a busca pode ser feita em trajetos de ida ou volta,
    # buscaremos rotas com:
    #    inicio = origem e fim = destino
    #ou
    #    fim = origem e inicio = destino
    # O resultado será ordenado com as rotas com meores distâncias aparecendo primeiro 
    rotas = Rota.select().where(
        (Rota.mapa == mapa) & (
            ((Rota.inicio == origem) & (Rota.fim == destino)) | 
            ((Rota.fim == origem) & (Rota.inicio == destino)) 
        )
    ).order_by(Rota.distancia)

    if len(rotas) > 0:
        # caso existam rotas que satisfaçam as condições fornecidas, 
        # a rota de menor distância será a primeira da lista, pois o 
        # resultado está ordenado pela menos distância
        rota = rotas[0]
        dist = rota.distancia
        # calculando o custo da rota com os valores de autonomia e preço do combustível fornecidos
        custo = "{:.2f}".format(round(float(valor_litro*dist)/float(autonomia), 2)).replace(".",",")
        # Teste para verificar como deve ser exibido o nome da rota
        # Ex. 
        # Rota encontrada A B C D
        # Se o ponto de origem informado foi o A, o nome apresentado será A B C D
        # Se o ponto de origem informado foi o D, o nome apresentado será D C B A
        if (rota.inicio == origem):
            nome_rota = rota.nome_rota
        else:
            nome_rota = rota.nome_rota[::-1]
        # Informando resultado para o cliente
        return {"status": 0, "message": "Rota "+nome_rota+" com custo de "+ custo}
    else:
        # Informar ao cliente que não foram encontradas rotas para os parâmetros fornecidos
        return {"status": 1, "message": u"Nenhuma rota encontrada para os parâmetros fornecidos".encode("ascii", "xmlcharrefreplace")}
