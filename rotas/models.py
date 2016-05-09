#!/usr/bin/python
# coding=utf-8
import peewee
from peewee import *
import ConfigParser

# Arquivo onde serão armazenados os dados das malhas
db = SqliteDatabase('.db/rotas.db')

############################################################################
# Função que cria as tabelas do BD caso seja a primeira execução do código #
############################################################################
def init():
	try:
		db.create_tables([Mapa, Rota]);
	except:
		pass

#####################################
# Classe base para os outros models #
#####################################
class BaseModel(Model):
    class Meta:
        database = db
		
##########################################
# Classe que define o modelo/tabela Mapa #
##########################################
class Mapa(BaseModel):
    id = PrimaryKeyField()
    nome_mapa = CharField()


##########################################
# Classe que define o modelo/tabela Rota #
##########################################
class Rota(BaseModel):
    id = PrimaryKeyField()
    nome_rota = CharField()
    inicio = CharField()
    fim = CharField()
    distancia = IntegerField()
    mapa = ForeignKeyField(Mapa)


