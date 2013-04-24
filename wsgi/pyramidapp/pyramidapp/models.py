from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
    )

import transaction

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import Column
from sqlalchemy import Text

from zope.sqlalchemy import ZopeTransactionExtension



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
    __tablename__ = 'Usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(Unicode(255), unique=True, nullable=False)
    senha = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    cep = Column(Text, nullable=False)
    idade = Column(Integer, nullable=False)
    celular = Column(Text, nullable=False)
    ano_Habilitacao = Column(Date, nullable=False)
    altura = Column(Double, nullable=False)
    peso = Column(Double, nullable=False)
    fumante = Column(Booleano, nullable=False)
    cachorro = Column(Integer, nullable=False)
    falante = Column(Booleano, nullable=False)
    data_Cadastro = Column(Date, nullable=False)
    id_Cidade = Column(Integer, ForeignKey('Cidade.id'))
    id_Estado = Column(Integer, ForeignKey('Estado.id'))
    id_Pais = Column(Integer, ForeignKey('Pais.id'))
    id_Hist_Avaliacoes = Column(Integer, ForeignKey('Historico_Avaliacoes.id'))
    id_Pref_Musicais = Column(Integer, ForeignKey('Preferencias_Musicais.id'))

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


class BdAutomoveis(Base):
    __tablename__ = 'Automoveis'
    id = Column(Integer, primary_key=True)
    ano = Column(Date, nullable=False)
    cor = Column(Text, nullable=False)
    placa = Column(Text, nullable=False)
    nro_Assentos = Column(Integer, nullable=False)
    id_Usuario = Column(Integer, ForeignKey('Usuarios.id'))
    estado_Usuario = Column(Integer, ForeignKey('Usuarios.estado'))
    pais_Usuario = Column(Integer, ForeignKey('Usuarios.pais'))

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
    __tablename__ = 'Rotas'
    id = Column(Integer, primary_key=True)
    data_Partida = Column(Date, nullable=False)
    data_Chegada = Column(Date, nullable=False)
    hora_Partida = Column(Date, nullable=False)
    hora_Chegada = Column(Date, nullable=False)
    frequencia = Column(Integer, nullable=False)
    possibilidade_desvio = Column(Booleano, nullable=False)
    tolerancia_atraso = Column(Date, nullable=False)
    id_Pais = Column(Integer, ForeignKey('Pais.id'))

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
    __tablename__ = 'Pais'
    id = Column(Integer, primary_key=True)
    nome = Column(Text, nullable=False)
    descricao = Column(Text, nullable=False)

    def __init__(self,
                 nome="",
                 descricao="",
                 grupo="g:usuario"):
        self.nome = nome
        self.descricao = descricao
        
class BdEstado(Base):
    __tablename__ = 'Estado'
    id = Column(Integer, primary_key=True)
    nome = Column(Text, nullable=False)
    descricao = Column(Text, nullable=False)

    def __init__(self,
                 nome="",
                 descricao="",
                 grupo="g:usuario"):
        self.nome = nome
        self.descricao = descricao
        
class BdCidade(Base):
    __tablename__ = 'Cidade'
    id = Column(Integer, primary_key=True)
    nome = Column(Text, nullable=False)
    descricao = Column(Text, nullable=False)

    def __init__(self,
                 nome="",
                 descricao="",
                 grupo="g:usuario"):
        self.nome = nome
        self.descricao = descricao


class BdPreferencias_Musicais(Base):
    __tablename__ = 'Preferencias_Musicais'
    id = Column(Integer, primary_key=True)
    nome_Artista = Column(Text, nullable=False)
    descricao_Artista = Column(Text, nullable=False)

    def __init__(self,
                 nome_Artista="",
                 descricao_Artista="",
                 grupo="g:usuario"):
        self.nome_Artista = nome_Artista
        self.descricao_Artista = descricao_Artista
        
        
class BdHistorico_Avaliacoes(Base):
    __tablename__ = 'Historico_Avaliacoes'
    id = Column(Integer, primary_key=True)
    nome_Artista = Column(Text, nullable=False)
    descricao_Artista = Column(Text, nullable=False)

    def __init__(self,
                 nome_Artista="",
                 descricao_Artista="",
                 grupo="g:usuario"):
        self.nome_Artista = nome_Artista
        self.descricao_Artista = descricao_Artista
        
class BdEstado_has_Rotas(Base):
    __tablename__ = 'Estado_has_Rotas'
    id_Estado = Column(Integer, ForeignKey('Estado.id'))
    id_Rota = Column(Integer, ForeignKey('Rotas.id'))
    
class BdCidade_has_Rotas(Base):
    __tablename__ = 'Estado_has_Rotas'
    id_Cidade = Column(Integer, ForeignKey('Cidade.id'))
    id_Rota = Column(Integer, ForeignKey('Rotas.id'))
    


    
    
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
