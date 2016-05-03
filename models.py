#!/usr/bin/python
import peewee
from peewee import *

db = MySQLDatabase('rotas', user='root', passwd='sgc123')

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

