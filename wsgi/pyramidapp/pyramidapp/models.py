#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Copyright 2013 Carona Sustentavel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#-----------------------------------------------------------------------------

import os

from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
    )

import transaction

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy import create_engine
from sqlalchemy import Unicode
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from zope.sqlalchemy import ZopeTransactionExtension

PASTA = "pyramidapp"


class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'logar'),
                (Allow, 'g:admin', ALL_PERMISSIONS),
                (Allow, 'g:moderador', 'moderar'),
                (Allow, 'g:usuario', 'usar'),
              ]
    def __init__(self, request):
        pass

class UserFactory(object):
    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

    def __getitem__(self, nome):
        dbsession = DBSession()
        usu = dbsession.query(BdUsuario).filter_by(nome=nome).first()
        usu.__parent__ = self
        usu.__name__ = nome
        return usu



DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class BdUsuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(Unicode(255), unique=True, nullable=False)
    senha = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    cep = Column(Text, nullable=False)
    idade = Column(Integer, nullable=False)
    celular = Column(Text, nullable=False)
    ano_Habilitacao = Column(Integer, nullable=False)
    altura = Column(Float, nullable=False)
    peso = Column(Float, nullable=False)
    fumante = Column(Boolean, nullable=False)
    cachorro = Column(Integer, nullable=False)
    falante = Column(Boolean, nullable=False)
    data_cadastro = Column(Date, nullable=False)

    id_cidade = Column(Integer, ForeignKey('cidade.id'))
    cidade = relationship("BdCidade")
    id_estado = Column(Integer, ForeignKey('estado.id'))
    estado = relationship("BdEstado")
    id_pais = Column(Integer, ForeignKey('pais.id'))
    pais = relationship("BdPais")
    id_hist_avaliacoes = Column(Integer, ForeignKey('historico_avaliacoes.id'))
    id_pref_musicais = Column(Integer, ForeignKey('preferencias_musicais.id'))

    automoveis = relationship("BdAutomoveis")

    @property
    def __acl__(self):
        return [
            (Allow, self.nome, 'usar'),
        ]

    def verif_senha(self, senha):
        return self.senha == senha

    def __init__(self,
                 nome="",
                 senha="",
                 email="",
                 cep="",
                 idade="",
                 celular="",
                 ano_Habilitacao="",
                 altura="",
                 peso="",
                 fumante="",
                 cachorro="",
                 falante="",
                 data_Cadastro="",
                 cidade=1,
                 estado=1,
                 pais=1,
                 grupo="g:usuario"):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.cep = cep
        self.idade = idade
        self.celular = celular
        self.ano_Habilitacao = ano_Habilitacao
        self.altura = altura
        self.peso = peso
        self.fumante = fumante
        self.cachorro = cachorro
        self.falante = falante
        self.data_Cadastro = data_Cadastro
        self.cidade = cidade
        self.estado = estado
        self.pais = pais


class BdAutomoveis(Base):
    __tablename__ = 'automoveis'
    id = Column(Integer, primary_key=True)
    ano = Column(Integer, nullable=False)
    cor = Column(Text, nullable=False)
    placa = Column(Text, nullable=False)
    nro_assentos = Column(Integer, nullable=False)

    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    #estado_usuario = Column(Integer, ForeignKey('usuarios.id_estado'))
    #pais_usuario = Column(Integer, ForeignKey('usuarios.id_pais'))

    def __init__(self,
                 ano="",
                 cor="",
                 placa="",
                 nro_Assentos="",
                 grupo="g:usuario"):
        self.ano = ano
        self.cor = cor
        self.placa = placa
        self.nro_Assentos = nro_Assentos


class BdRotas(Base):
    __tablename__ = 'rotas'
    id = Column(Integer, primary_key=True)
    data_partida = Column(Date, nullable=False)
    data_chegada = Column(Date, nullable=False)
    hora_partida = Column(Date, nullable=False)
    hora_chegada = Column(Date, nullable=False)
    frequencia = Column(Integer, nullable=False)
    possibilidade_desvio = Column(Boolean, nullable=False)
    tolerancia_atraso = Column(Date, nullable=False)
    id_pais = Column(Integer, ForeignKey('pais.id'))

    def __init__(self,
                 data_Partida="",
                 data_Chegada="",
                 hora_Partida="",
                 hora_Chegada="",
                 frequencia="",
                 possibilidade_desvio="",
                 tolerancia_atraso="",
                 grupo="g:usuario"):
        self.data_Partida = data_Partida
        self.data_Chegada = data_Chegada
        self.hora_Partida = hora_Partida
        self.hora_Chegada = hora_Chegada
        self.frequencia = frequencia
        self.possibilidade_desvio = possibilidade_desvio
        self.tolerancia_atraso = tolerancia_atraso
        
class BdPais(Base):
    __tablename__ = 'pais'
    id = Column(Integer, primary_key=True)
    nome = Column(Text, nullable=False)
    descricao = Column(Text, nullable=False)
    usuarios = relationship("BdUsuario")
    rotas = relationship("BdRotas", uselist=False, backref="pais")

    def __init__(self,
                 nome="",
                 descricao="",
                 grupo="g:usuario"):
        self.nome = nome
        self.descricao = descricao
        
estado_has_rotas = Table('Estado_has_Rotas', Base.metadata,
    Column('id_Estado', Integer, ForeignKey('estado.id')),
    Column('id_Rota', Integer, ForeignKey('rotas.id'))
)

cidade_has_rotas = Table('Cidade_has_Rotas', Base.metadata,
    Column('id_Cidade', Integer, ForeignKey('cidade.id')),
    Column('id_Rota', Integer, ForeignKey('rotas.id'))
)

class BdEstado(Base):
    __tablename__ = 'estado'
    id = Column(Integer, primary_key=True)
    nome = Column(Text, nullable=False)
    descricao = Column(Text, nullable=False)
    usuarios = relationship("BdUsuario")
    rotas = relationship("BdRotas", secondary=estado_has_rotas, backref="estado")

    def __init__(self,
                 nome="",
                 descricao="",
                 grupo="g:usuario"):
        self.nome = nome
        self.descricao = descricao
        
class BdCidade(Base):
    __tablename__ = 'cidade'
    id = Column(Integer, primary_key=True)
    nome = Column(Text, nullable=False)
    descricao = Column(Text, nullable=False)
    usuarios = relationship("BdUsuario")
    rotas = relationship("BdRotas", secondary=cidade_has_rotas, backref="cidade")

    def __init__(self,
                 nome="",
                 descricao="",
                 grupo="g:usuario"):
        self.nome = nome
        self.descricao = descricao


class BdPreferencias_Musicais(Base):
    __tablename__ = 'preferencias_musicais'
    id = Column(Integer, primary_key=True)
    nome_Artista = Column(Text, nullable=False)
    descricao_Artista = Column(Text, nullable=False)
    usuarios = relationship("BdUsuario")

    def __init__(self,
                 nome_Artista="",
                 descricao_Artista="",
                 grupo="g:usuario"):
        self.nome_Artista = nome_Artista
        self.descricao_Artista = descricao_Artista
        
        
class BdHistorico_Avaliacoes(Base):
    __tablename__ = 'historico_avaliacoes'
    id = Column(Integer, primary_key=True)
    nota = Column(Integer, nullable=False)
    descricao_Nota = Column(Text, nullable=False)
    usuarios = relationship("BdUsuario")

    def __init__(self,
                 nome_Artista="",
                 descricao_Artista="",
                 grupo="g:usuario"):
        self.nome_Artista = nome_Artista
        self.descricao_Artista = descricao_Artista
        
        
#class BdEstado_has_Rotas(Base):
#    __tablename__ = 'Estado_has_Rotas'
#    id = Column(Integer, primary_key=True)
#    id_Estado = Column(Integer, ForeignKey('Estado.id'))
#    id_Rota = Column(Integer, ForeignKey('Rotas.id'))
    
#class BdCidade_has_Rotas(Base):
#    __tablename__ = 'Cidade_has_Rotas'
#    id = Column(Integer, primary_key=True)
#    id_Cidade = Column(Integer, ForeignKey('Cidade.id'))
#    id_Rota = Column(Integer, ForeignKey('Rotas.id'))
    

def populate():
    #Locais
    session = DBSession()
    pasta = os.path.join(PASTA,"locais")
    tipos = {"paises": BdPais,
             "estados": BdEstado,
             "cidades": BdCidade}
    for arquivo,classe in tipos.items():
        arq = open(os.path.join(pasta,arquivo))
        lista = arq.read().splitlines()
        arq.close()
        for linha in lista:
            linha = unicode(linha.strip(),"utf8")
            modelo = classe(nome=linha)
            session.add(modelo)

    model = BdUsuario(nome='test', senha="11111")
    session.add(model)
    session.flush()
    transaction.commit()

    
def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        DBSession.rollback()
    
#class MyModel(Base):
#    __tablename__ = 'models'
#    id = Column(Integer, primary_key=True)
#    name = Column(Unicode(255), unique=True)
#    value = Column(Integer)
#
#    def __init__(self, name, value):
#        self.name = name
#        self.value = value
#
#class MyApp(object):
#    __name__ = None
#    __parent__ = None
#
#    def __getitem__(self, key):
#        session= DBSession()
#        try:
#            id = int(key)
#        except (ValueError, TypeError):
#            raise KeyError(key)
#
#        query = session.query(MyModel).filter_by(id=id)
#
#        try:
#            item = query.one()
#            item.__parent__ = self
#            item.__name__ = key
#            return item
#        except NoResultFound:
#            raise KeyError(key)
#
#    def get(self, key, default=None):
#        try:
#            item = self.__getitem__(key)
#        except KeyError:
#            item = default
#        return item
#
#    def __iter__(self):
#        session= DBSession()
#        query = session.query(MyModel)
#        return iter(query)
#
#root = MyApp()
#
#def default_get_root(request):
#    return root
#
#def populate():
#    session = DBSession()
#    model = MyModel(name=u'test name', value=55)
#    session.add(model)
#    session.flush()
#    transaction.commit()
#
#def initialize_sql(engine):
#    DBSession.configure(bind=engine)
#    Base.metadata.bind = engine
#    Base.metadata.create_all(engine)
#    try:
#        populate()
#    except IntegrityError:
#        DBSession.rollback()
#
#def appmaker(engine):
#    initialize_sql(engine)
#    return default_get_root
