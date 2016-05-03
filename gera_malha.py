#!/usr/bin/python
from models import *

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
                arrRes[nkey]["auto"] = int(itens[2])
                arrRes[nkey]["auto_last"] = int(itens[2])
                arrRes[nkey]["dist"] = int(itens[2])
                if (end in ref):
                    buscaRota(linhas, ref, end, index+1, arrRes, nkey)
        else:
            if (start == last and end not in key):
                nkey = key+" "+end
		arrRes[nkey] = dict()
                arrRes[nkey]["inicio"] = arrRes[key]["inicio"]
                arrRes[nkey]["fim"] = end
                arrRes[nkey]["auto"] = arrRes[key]["auto"]
                arrRes[nkey]["auto_last"] = int(itens[2])
                arrRes[nkey]["dist"] = arrRes[key]["dist"] + int(itens[2])
                if (end in ref):
		    buscaRota(linhas, ref, end, index+1, arrRes, nkey)

nome_mapa = "rj";
malha  = """a b 1
a c 2
a d 3
b c 1
b d 2
c d 1
a e 2
a f 3
a g 4
a h 5
a i 6
a j 7
b e 3
b f 2
b g 3
b h 4
b i 5
b j 6
c e 4
c f 3
c g 2
c h 3
c i 4
c j 5
d e 5
d f 4
d g 3
d h 2
d i 3
d j 4
e k 2
e l 3
e m 4
e n 5
e o 6
e p 7
e q 8
e r 9
f k 3
f l 2
f m 3
f n 4
f o 5
f p 6
f q 7
f r 8
g k 4
g l 3
g m 2
g n 3
g o 4
g p 5
g q 6
g r 7
h k 5
h l 4
h m 3
h n 2
h o 3
h p 4
h q 5
h r 6
i k 6
i l 5
i m 4
i n 3
i o 2
i p 3
i q 4
i r 5
j k 7
j l 6
j m 5
j n 4
j o 3
j p 2
j q 3
j r 4
k s 2
k t 3
k u 4
k v 5
l s 3
l t 2
l u 3
l v 4
m s 4
m t 3
m u 2
m v 3
n s 5
n t 4
n u 3
n v 2
o s 6
o t 5
o u 4
o v 3
p s 7
p t 6
p u 5
p v 4
q s 8
q t 7
q u 6
q v 5
r s 9
r t 8
r u 7
r v 6
s x 3
s z 4
t x 2
t z 3
u x 3
u z 2
v x 4
v z 3
x z 1"""

mapasDB = Mapa.filter(nome_mapa = nome_mapa)
if (len(mapasDB) == 0):
    mapa = Mapa(nome_mapa=nome_mapa)
    mapa.save()
else:
    mapa = mapasDB[0]
    print "mapa ja cadastrado"

lines = malha.splitlines()
lines.sort()
ref = []
for line in lines:
    ref.append(line[0])

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
        'autonomia' : arrRes[nome]["auto"],
        'autonomia_ultima' : arrRes[nome]["auto_last"],
        'distancia' : arrRes[nome]["dist"],
        'id_mapa' : mapa.id
    })

with db.atomic():
    for idx in range(0, len(data_source), 1000):
        Rota.insert_many(data_source[idx:idx+1000]).execute()
