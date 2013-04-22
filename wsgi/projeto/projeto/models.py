from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
    )


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
    __tablename__ = 'usar'
    id = Column(Integer, primary_key=True)
    #id = Column(mysql.BIGINT(20, unsigned=True), primary_key=True, autoincrement=True)
    nome = Column(Text, unique=True, nullable=False)
    senha = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    cidade = Column(Text, nullable=False)
    estado = Column(Text, nullable=False)
    cep = Column(Text, nullable=False)
    idade = Column(Integer, nullable=False)

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
                 cidade="",
                 estado="",
                 cep="",
                 idade="",
                 grupo="g:usuario"):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.idade = idade
