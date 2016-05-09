# coding=utf-8

############################################################
# Função para verificar se uma string representa um número #
############################################################
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#####################################################################
# Função recursiva para buscar rotas a partir de um ponto de origem #
#####################################################################
def buscaRota(linhas, ref, last, index, arrRes, key = ""):
    # filtrando apenas as linhas que começam com o ponto de origem informado
    linhasUteis = linhas[ref.index(last):(len(ref) - ref[::-1].index(last))]
    for linha in linhasUteis:
        itens = linha.split()
        start = itens[0]
        end = itens[1]
        if (index == 0):
            # Como esta é a primeira chamada dessa função, a chave, que é o nome da rota, ainda não existe no dicionário
            # Vamos então criá-la e informar os pontos de inicio e fim, assim como a distância para essa rota
            nkey = start+" "+end
            arrRes[nkey] = dict()
            arrRes[nkey]["inicio"] = itens[0]
            arrRes[nkey]["fim"] = itens[1]
            arrRes[nkey]["dist"] = int(itens[2])
            # Caso exista alguma rota iniciada pelo ponto de destino da rota atual, 
            # faremos nova chamada a essa função para buscar essas novas rotas complementares
            if (end in ref):
                buscaRota(linhas, ref, end, index+1, arrRes, nkey)
        else:
            # Não estamos mais na primeira chamada dessa função
            # Estamos buscando rotas complementares às indicadas na malha.
            if (start == last and end not in key):
                # Caso a origem dessa rota coincida com o destino da rota anterior,
                # complementaremos a rota com mais esse ponto
                # Ex.
                # A rota anterior foi A B 10.
                # Essa rota é B C 5
                # Vamos então armazenar a rota A B C 15
                nkey = key+" "+end
                arrRes[nkey] = dict()
                arrRes[nkey]["inicio"] = arrRes[key]["inicio"]
                arrRes[nkey]["fim"] = end
                arrRes[nkey]["dist"] = arrRes[key]["dist"] + int(itens[2])
                # Caso exista alguma rota iniciada pelo ponto de destino da rota atual, 
                # faremos nova chamada a essa função para buscar essas novas rotas complementares
                if (end in ref):
                    buscaRota(linhas, ref, end, index+1, arrRes, nkey)

