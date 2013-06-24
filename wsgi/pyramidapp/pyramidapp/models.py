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
import datetime


from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
)

from pyramid.path import AssetResolver

import transaction

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.exc import IntegrityError
#from sqlalchemy.orm.exc import NoResultFound

#from sqlalchemy import create_engine
from sqlalchemy import (
    ForeignKey,
    Integer,
    Boolean,
    Unicode,
    Column,
    Table,
    Float,
    Text,
    Time,
    Date,
)

from zope.sqlalchemy import ZopeTransactionExtension


class RootFactory(object):
    __acl__ = [(Allow, Everyone, 'logar'),
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
    senha = Column(Unicode(255), nullable=False)
    email = Column(Text, nullable=False)
    cep = Column(Text, nullable=False)

    idade = Column(Integer, nullable=False)
    celular = Column(Text, nullable=False)
    ano_habilitacao = Column(Integer, nullable=False)
    altura = Column(Float, nullable=False)
    peso = Column(Float, nullable=False)
    fumante = Column(Boolean, nullable=False)
    cachorro = Column(Boolean, nullable=False)
    falante = Column(Boolean, nullable=False)
    data_cadastro = Column(Date, nullable=False)

    cidade = Column(Text, nullable=False)
    estado = Column(Text, nullable=False)
    pais = Column(Text, nullable=False)

    #id_cidade = Column(Integer, ForeignKey('cidades.id'))
    #cidade = relationship("BdCidade")
    #id_estado = Column(Integer, ForeignKey('estados.id'))
    #estado = relationship("BdEstado")
    #id_pais = Column(Integer, ForeignKey('paises.id'))
    #pais = relationship("BdPais")
    id_hist_avaliacoes = Column(Integer, ForeignKey('historico_avaliacoes.id'))
    id_pref_musicais = Column(Integer, ForeignKey('preferencias_musicais.id'))

    automoveis = relationship("BdAutomovel")

    @property
    def __acl__(self):
        return [
            (Allow, self.nome, 'usar'),
        ]

    def verif_senha(self, senha):
        return self.senha == senha

    def __init__(self,
                 nome=None,
                 senha=None,
                 email=None,
                 cep=None,
                 idade=None,
                 celular=None,
                 ano_habilitacao=None,
                 altura=None,
                 peso=None,
                 fumante=None,
                 cachorro=None,
                 falante=None,
                 data_cadastro=None,
                 cidade=None,
                 estado=None,
                 pais=None,
                 grupo="g:usuario"):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.cep = cep
        self.idade = idade
        self.celular = celular
        self.ano_habilitacao = ano_habilitacao
        self.altura = altura
        self.peso = peso
        self.fumante = fumante
        self.cachorro = cachorro
        self.falante = falante
        self.data_cadastro = data_cadastro
        self.cidade = cidade
        self.estado = estado
        self.pais = pais


class BdAutomovel(Base):
    __tablename__ = 'automoveis'
    id = Column(Integer, primary_key=True)
    usuario = Column(Integer, ForeignKey('usuarios.nome'), nullable=False)
    ano = Column(Integer, nullable=False)
    cor = Column(Text, nullable=False)
    placa = Column(Text, nullable=False)
    nro_assentos = Column(Integer, nullable=False)

    def __init__(self,
                 usuario=None,
                 ano=None,
                 cor=None,
                 placa=None,
                 nro_assentos=None,
                 grupo="g:usuario"):
        self.usuario = usuario
        self.ano = ano
        self.cor = cor
        self.placa = placa
        self.nro_assentos = nro_assentos


class BdCarona(Base):
    __tablename__ = 'rotas'
    id = Column(Integer, primary_key=True)
    usuario = Column(Integer, ForeignKey('usuarios.nome'), nullable=False)
    local_partida = Column(Text, nullable=False)
    local_chegada = Column(Text, nullable=False)
    data_partida = Column(Text, nullable=False)
    data_chegada = Column(Text, nullable=False)
    hora_partida = Column(Text, nullable=False)
    hora_chegada = Column(Text, nullable=False)
    frequencia = Column(Text, nullable=False)
    tolerancia_atraso = Column(Text, nullable=False)
    possibilidade_desvio = Column(Text, nullable=False)
    id_pais = Column(Integer, ForeignKey('paises.id'))

    def __init__(self,
                 usuario=None,
                 local_partida=None,
                 local_chegada=None,
                 data_partida=None,
                 data_chegada=None,
                 hora_partida=None,
                 hora_chegada=None,
                 frequencia=None,
                 possibilidade_desvio=None,
                 tolerancia_atraso=None,
                 grupo="g:usuario"):
        self.usuario = usuario
        self.local_partida = local_partida
        self.local_chegada = local_chegada
        self.data_partida = data_partida
        self.data_chegada = data_chegada
        self.hora_partida = hora_partida
        self.hora_chegada = hora_chegada
        self.frequencia = frequencia
        self.possibilidade_desvio = possibilidade_desvio
        self.tolerancia_atraso = tolerancia_atraso


estado_has_rotas = Table('Estado_has_Rotas', Base.metadata,
                         Column('id_Estado', Integer,
                                ForeignKey('estados.id')),
                         Column('id_Rota', Integer,
                                ForeignKey('rotas.id'))
                         )

cidade_has_rotas = Table('Cidade_has_Rotas', Base.metadata,
                         Column('id_Cidade', Integer,
                                ForeignKey('cidades.id')),
                         Column('id_Rota', Integer,
                                ForeignKey('rotas.id'))
                         )


class BdPais(Base):
    __tablename__ = 'paises'
    id = Column(Integer, primary_key=True)
    nome = Column(Unicode(255), nullable=False)
    descricao = Column(Text, nullable=True)
    #usuarios = relationship("BdUsuario")
    rotas = relationship("BdCarona", uselist=False, backref="paises")

    def __init__(self,
                 nome=None,
                 descricao=None,
                 grupo="g:usuario"):
        self.nome = nome
        self.descricao = descricao


class BdEstado(Base):
    __tablename__ = 'estados'
    id = Column(Integer, primary_key=True)
    nome = Column(Unicode(255), nullable=False)
    descricao = Column(Text, nullable=True)
    #usuarios = relationship("BdUsuario")
    rotas = relationship("BdCarona", secondary=estado_has_rotas,
                         backref="estados")

    def __init__(self,
                 nome=None,
                 descricao=None,
                 grupo="g:usuario"):
        self.nome = nome
        self.descricao = descricao


class BdCidade(Base):
    __tablename__ = 'cidades'
    id = Column(Integer, primary_key=True)
    nome = Column(Unicode(255), nullable=False)
    descricao = Column(Text, nullable=True)
    #usuarios = relationship("BdUsuario")
    rotas = relationship("BdCarona", secondary=cidade_has_rotas,
                         backref="cidades")

    def __init__(self,
                 nome=None,
                 descricao=None,
                 grupo="g:usuario"):
        self.nome = nome
        self.descricao = descricao


class BdPreferencia_Musical(Base):
    __tablename__ = 'preferencias_musicais'
    id = Column(Integer, primary_key=True)
    nome_Artista = Column(Unicode(255), nullable=False)
    descricao_Artista = Column(Text, nullable=False)
    usuarios = relationship("BdUsuario")

    def __init__(self,
                 nome_Artista=None,
                 descricao_Artista=None,
                 grupo="g:usuario"):
        self.nome_Artista = nome_Artista
        self.descricao_Artista = descricao_Artista


class BdHistorico_Avaliacoes(Base):
    __tablename__ = 'historico_avaliacoes'
    id = Column(Integer, primary_key=True)
    nota = Column(Unicode(255), nullable=False)
    descricao_Nota = Column(Text, nullable=False)
    usuarios = relationship("BdUsuario")

    def __init__(self,
                 nome_Artista=None,
                 descricao_Artista=None,
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
    asset = AssetResolver('pyramidapp')
    pasta = "locais"
    tipos = {"paises": BdPais,
             "estados": BdEstado,
             "cidades": BdCidade}
    for arquivo, classe in tipos.items():
        resolver = asset.resolve(os.path.join(pasta, arquivo))
        arq = open(resolver.abspath())
        lista = arq.read().splitlines()
        arq.close()
        for linha in lista:
            linha = unicode(linha.strip(), "utf8")
            modelo = classe(nome=linha)
            session.add(modelo)
    session.flush()
    transaction.commit()

    model = BdUsuario(nome='test',
                      senha="11111",
                      email="a@a.com",
                      cep="123",
                      cidade="123",
                      estado="12",
                      pais="12",
                      idade="1",
                      celular="1",
                      ano_habilitacao="1",
                      altura="1",
                      peso="1",
                      fumante=False,
                      cachorro=True,
                      falante=True,
                      data_cadastro=datetime.date.today(),
                      )
    session.add(model)
    session.flush()
    transaction.commit()

    model = BdUsuario(nome='bolha',
                      senha="11111",
                      email="a@a.com",
                      cep="123",
                      cidade="123",
                      estado="12",
                      pais="12",
                      idade="1",
                      celular="1",
                      ano_habilitacao="1",
                      altura="1",
                      peso="1",
                      fumante=False,
                      cachorro=True,
                      falante=True,
                      data_cadastro=datetime.date.today(),
                      )
    session.add(model)
    session.flush()
    transaction.commit()

    model = BdCarona(
                     usuario='test',
                     local_partida="C",
                     local_chegada="B",
                     data_partida=datetime.date(1,2,3),
                     data_chegada=datetime.date(1,2,3),
                     hora_partida=datetime.time(1,2),
                     hora_chegada=datetime.time(1,2),
                     frequencia="nenhuma",
                     possibilidade_desvio="nem a pau",
                     tolerancia_atraso="capaiz!",
                  )
    session.add(model)
    model = BdCarona(
                     usuario='bolha',
                     local_partida="A",
                     local_chegada="B",
                     data_partida=datetime.date(1,2,4),
                     data_chegada=datetime.date(1,3,3),
                     hora_partida=datetime.time(2,2),
                     hora_chegada=datetime.time(3,2),
                     frequencia="toda",
                     possibilidade_desvio="claro!",
                     tolerancia_atraso="da nada nao",
                  )
    session.add(model)
    model = BdAutomovel(
                     usuario='bolha',
                 ano=1800,
                 cor="rosa choque",
                 placa="a23h923u",
                 nro_assentos=100,
                  )
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
