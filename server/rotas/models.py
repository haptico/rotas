#!/usr/bin/python
import peewee
from peewee import *
import ConfigParser

#cp = ConfigParser.ConfigParser()
#try:
#    fileset = cp.read("config/db.ini")
#    if len(fileset) == 0:
#        raise ValueError
#except:
#    print "Arquivo de configuracao 'config/db.ini' nao encontrado. Abortando..."
#    exit()

#host = cp.get("Database","host")
#port = int(cp.get("Database","port"))
#user = cp.get("Database","user")
#password = cp.get("Database","password")
#schema = cp.get("Database","schema")

db = SqliteDatabase('rotas.db')


def init():
	try:
		db.create_tables([Mapa, Rota]);
	except:
		pass
	
class BaseModel(Model):
    class Meta:
        database = db
		
class Mapa(BaseModel):
    id = PrimaryKeyField()
    nome_mapa = CharField()


class Rota(BaseModel):
    id = PrimaryKeyField()
    nome_rota = CharField()
    inicio = CharField()
    fim = CharField()
    distancia = IntegerField()
    mapa = ForeignKeyField(Mapa)


