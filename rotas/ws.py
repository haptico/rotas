 # coding=utf-8
import models
from models import *

models.init()

def buscaRota(linhas, ref, last, index, arrRes, key = ""):
    linhasUteis = linhas[ref.index(last):(len(ref) - ref[::-1].index(last))]
    for linha in linhasUteis:
        itens = linha.split()
        start = itens[0]
        end = itens[1]
        if (index == 0):
            nkey = start+" "+end
            if (end+" "+start not in arrRes):
                arrRes[nkey] = dict()
                arrRes[nkey]["inicio"] = itens[0]
                arrRes[nkey]["fim"] = itens[1]
                arrRes[nkey]["dist"] = int(itens[2])
                if (end in ref):
                    buscaRota(linhas, ref, end, index+1, arrRes, nkey)
        else:
            if (start == last and end not in key):
                nkey = key+" "+end
                arrRes[nkey] = dict()
                arrRes[nkey]["inicio"] = arrRes[key]["inicio"]
                arrRes[nkey]["fim"] = end
                arrRes[nkey]["dist"] = arrRes[key]["dist"] + int(itens[2])
                if (end in ref):
                    buscaRota(linhas, ref, end, index+1, arrRes, nkey)

def geraMalha(inputMapa, inputMalha):
    linhas = inputMalha.strip().splitlines()
    linhas.sort()
    ref = []
    lines = []
    for linha in linhas:
        itens = linha.strip().split()
        if (len(itens) != 3):
            return {"status": 1, "message": "A linha '"+linha+u"' da malha não está no formato esperado: '<origem> <destino> <distância>'. A malha não foi importada.".encode("ascii", "xmlcharrefreplace")}
        lines.append(linha.strip())
        ref.append(itens[0])

    if (inputMapa['id'] == 0):
        mapa = Mapa(nome_mapa=inputMapa['nome'])
        mapa.save()
    else:
        mapa = Mapa(id=inputMapa["id"], nome_mapa=inputMapa["nome"])
        q = Rota.delete().where(Rota.mapa == mapa)
        q.execute()
		
    arrRes = dict()
    for line in lines:
        itens = line.split()
        inicio = itens[0]
        buscaRota(lines, ref, inicio, 0, arrRes)

    data_source = []
    for nome in arrRes:
        data_source.append({
            'nome_rota' : nome,
            'inicio' : arrRes[nome]["inicio"],
            'fim' : arrRes[nome]["fim"],
            'distancia' : arrRes[nome]["dist"],
            'mapa' : mapa
        })
    with db.atomic():
        for idx in range(0, len(data_source), 1000):
            Rota.insert_many(data_source[idx:idx+1000]).execute()
			
    return {"status": 0, "message": "Malha importada com sucesso!"}

def checaMapa(mapa):
	mapasDB = Mapa.filter(nome_mapa = mapa)
	if (len(mapasDB) == 0):
		return {"status": 0, "message": "Novo Mapa", "mapa": {"id": 0, "nome": mapa}}
	else:
		mapa = mapasDB[0]
		return {"status": 1, "message": "Mapa Existente", "mapa": {"id": mapa.id, "nome": mapa.nome_mapa}}

		
def consultaRota(inputMapa, origem, destino, autonomia, valor_litro):
	mapasDB = Mapa.filter(nome_mapa = inputMapa)
	if (len(mapasDB) == 0):
		return {"status": 1, "message": u"Mapa não encontrado".encode("ascii", "xmlcharrefreplace")}
	else:
		mapa = mapasDB[0]

	rotas = Rota.select().where(
		(Rota.mapa == mapa) & (
			((Rota.inicio == origem) & (Rota.fim == destino)) | 
			((Rota.fim == origem) & (Rota.inicio == destino)) 
		)
	).order_by(Rota.distancia)
	
	if len(rotas) > 0:
		rota = rotas[0]
		dist = rota.distancia
		custo = "{:.2f}".format(round(float(valor_litro*dist)/float(autonomia), 2)).replace(".",",")
		if (rota.inicio == origem):
			nome_rota = rota.nome_rota
		else:
			nome_rota = rota.nome_rota[::-1]
					
		return {"status": 0, "message": "Rota "+nome_rota+" com custo de "+ custo}
	else:
		return {"status": 1, "message": u"Nenhuma rota encontrada para os parâmetros fornecidos".encode("ascii", "xmlcharrefreplace")}
			
if __name__ == "__main__":
	m = 'sp'
	mal = """A B 10
B D 15
A C 20
C D 30
B E 50
D E 30"""
	r = checaMapa('sp')
	print r
	res = consultaRota("SP", "D", "A", 10, 2.5)
	print res
	