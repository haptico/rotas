#!/usr/bin/python
import peewee
from peewee import *
import ConfigParser

cp = ConfigParser.ConfigParser()
try:
    fileset = cp.read("config/db.ini")
    if len(fileset) == 0:
        raise ValueError
except:
    print "Arquivo de configuracao 'config/db.ini' nao encontrado. Abortando..."
    exit()

host = cp.get("Database","host")
port = int(cp.get("Database","port"))
user = cp.get("Database","user")
password = cp.get("Database","password")
schema = cp.get("Database","schema")

db = MySQLDatabase(schema, host=host, port=port, user=user, passwd=password)

class Mapa(peewee.Model):
    id = peewee.PrimaryKeyField()
    nome_mapa = peewee.CharField()

    class Meta:
        database = db

class Rota(peewee.Model):
    id = peewee.PrimaryKeyField()
    nome_rota = peewee.CharField()
    inicio = peewee.CharField()
    fim = peewee.CharField()
    autonomia = peewee.IntegerField()
    autonomia_ultima = peewee.IntegerField()
    distancia = peewee.IntegerField()
    id_mapa = peewee.IntegerField()

    class Meta:
        database = db

