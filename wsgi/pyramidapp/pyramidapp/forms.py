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

from deform import widget, Form
from colander import (
    MappingSchema,
    SchemaNode,
    Function,
    Boolean,
    Mapping,
    Integer,
    String,
    Length,
    Float,
    Email,
    Date,
    Time,
)

from .models import DBSession, BdUsuario


def record_to_appstruct(self):
    #form =  formulador(FormRegistrar,('Registrar',))
    return dict([(k, self.__dict__[k]) for k in sorted(self.__dict__) if '_sa_' != k[:4]])


def merge_session_with_post(session, post):
    for key, value in post:
        setattr(session, key, value)
    return session


def formulador(form, botoes):
    f = {"form": Form(form(), buttons=botoes).render()}
    return f


def verif_nome_unico(nome):
    dbsession = DBSession()
    j = dbsession.query(BdUsuario).filter_by(nome=nome).first()
    if j is None:
        return True
    else:
        return False


class FormLogin(MappingSchema):
    nome = SchemaNode(
                    String(),
                    description='Digite seu nome de usuário')
    senha = SchemaNode(
                       String(),
                       validator=Length(min=5, max=100),
                       widget=widget.PasswordWidget(size=20),
                       description='Digite sua senha')

class FormRegistrar(MappingSchema):
    nome = SchemaNode(
                      String(),
                      validator=Function(verif_nome_unico,"Nome existe"),
                      description='Digite seu nome de usuário')
    senha = SchemaNode(
                String(),
                validator=Length(min=5),
                widget=widget.CheckedPasswordWidget(size=20),
                description='Digite sua senha e a confirme')
    email = SchemaNode(
                String(),
                validator=Email('Email inválido'))
    cidade = SchemaNode(String(),
                description='Digite o nome de sua cidade')
    estado = SchemaNode(String(),
                validator=Length(max=2,min=2),
                description='Digite a sigla de seu estado')
    cep = SchemaNode(String(),
                description='Digite o número de seu CEP')
    idade = SchemaNode(Integer(),
                description='Digite sua idade')
    celular = SchemaNode(Integer(),
                description='Digite seu celular')
    ano_habilitacao = SchemaNode(Integer(),
                description='Digite o ano em que tirou sua habilitação')
    altura = SchemaNode(Float(),
                description='Digite sua altura')
    peso = SchemaNode(Float(),
                description='Digite seu peso')
    fumante = SchemaNode(Boolean(),
                description='Você fuma?')
    cachorro = SchemaNode(Boolean(),
                description='Você tem cachorro?')
    falante = SchemaNode(Boolean(),
                description='Você fala muito?')

class FormEditar(MappingSchema):
    senha = SchemaNode(
                String(),
                validator=Length(min=5),
                widget=widget.CheckedPasswordWidget(size=20),
                description='Digite sua senha e a confirme')
    email = SchemaNode(
                String(),
                validator=Email('Email inválido'))
    cidade = SchemaNode(String(),
                description='Digite o nome de sua cidade')
    estado = SchemaNode(String(),
                validator=Length(max=2,min=2),
                description='Digite a sigla de seu estado')
    cep = SchemaNode(String(),
                description='Digite o número de seu CEP')
    idade = SchemaNode(Integer(),
                description='Digite sua idade')

class FormAutomovel(MappingSchema):
    cor = SchemaNode(String(),
                     description='Cor')
    ano = SchemaNode(Integer(),
                     description='Ano')
    placa = SchemaNode(String(),
                       description='Placa')
    nro_assentos = SchemaNode(Integer(),
                            description='Número de assentos')

class FormRota(MappingSchema):
    data_partida = SchemaNode(Date(),
                     description='Data de partida')
    data_chegada = SchemaNode(Date(),
                     description='Data de chegada')
    hora_partida = SchemaNode(Time(),
                     description='Hora de partida')
    hora_chegada = SchemaNode(Time(),
                     description='Hora de chegada')
    frequencia = SchemaNode(String(),
                       description='Frequencia da Rota')
    possibilidade_desvio = SchemaNode(String(),
                       description='Possibilidade de se fazer desvio na rota')
    tolerancia_atraso = SchemaNode(String(),
                       description='Tolerância com possíveis atrasos')
