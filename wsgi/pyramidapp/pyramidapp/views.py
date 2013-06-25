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

from datetime import date, time
from collections import OrderedDict

import json

from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget, authenticated_userid
#from sqlalchemy import DBAPIError
import deform

from .models import (
    DBSession,
    BdUsuario,
    BdAutomovel,
    BdCarona,
    )

from forms import *


def tratar_tempo(dicio):
    pass
#    separador = '-'
#    for tipo in ["data_partida","data_chegada"]:
#        a,b,c = dicio[tipo].split(separador)
#        a, b, c = int(a), int(b), int(c)
#        dicio[tipo] = date(c,b,a)
#    separador = ':'
#    for tipo in ["hora_partida","hora_chegada"]:
#        lista = dicio[tipo].split(separador)
#        lista2 = [int(a) for a in lista]
#        dicio[tipo] = time(*lista2)


@forbidden_view_config(renderer='proibida.slim')
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    logado = authenticated_userid(request)
    if logado:
        return {'logado':logado}
    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)


@view_config(route_name='inicial', renderer='inicial.slim')
def inicial(request):
    usuario = authenticated_userid(request)
    if usuario:
        return HTTPFound(location = request.route_url('ver_perfil', id=usuario))
    else:
        return HTTPFound(location = request.route_url('login'))
    #return {"usuario":usuario}

@view_config(route_name='login', renderer='login.slim')
def pagina_login(request):
    next = request.params.get('next') or request.route_url('inicial')
    login_url = request.route_url('login')
    form = deform.Form(FormLogin(), buttons=('Entrar',))
    if 'Entrar' in request.POST:
        try:
            appstruct = form.validate(request.POST.items())
        except deform.ValidationFailure, e:
            return {'form':e.render()}
        nome = request.POST.get("nome",'')
        senha = request.POST.get("senha",'')
        dbsession = DBSession()
        jog = dbsession.query(BdUsuario).filter_by(nome=nome).first()
        if jog and jog.verif_senha(senha):
            headers = remember(request, nome)
            return HTTPFound(location=next, headers=headers)
        mensagem = 'Falha no login'
        return {'form':form.render(appstruct={'nome':nome,'senha':senha}),
                'mensagem' : mensagem,
                'url' : request.application_url + '/login',
                #'came_from' : came_from,
               }
    return {'form':form.render()}

@view_config(route_name='logout', permission='usar')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('inicial'), headers = headers)


@view_config(route_name='criar_perfil', renderer='registrar.slim')
def criar_perfil(request):
    """Registro de usuário"""
    form = deform.Form(FormRegistrar(), buttons=('Registrar',))
    if 'Registrar' in request.POST:
        try:
            appstruct = form.validate(request.POST.items())
        except deform.ValidationFailure, e:
            return {'form':e.render()}
        dbsession = DBSession()

        atribs = request.POST
        nome = atribs["nome"]
        senha = atribs["senha"]

        record = BdUsuario(nome, senha)
        record = merge_session_with_post(record, appstruct.items())
        record.data_cadastro = date.today()
        dbsession.merge(record)
        dbsession.flush()
        return HTTPFound(location = request.route_url('login'))
    return {'form':form.render()}

@view_config(route_name='ver_perfil', renderer='ver_perfil.slim')
def ver_perfil(request):
    """Ver perfil de usuário"""
    usuario = authenticated_userid(request)
    dbsession = DBSession()
    id = request.matchdict.get('id')
    if id:
        record = dbsession.query(BdUsuario).filter_by(nome=id).first()
    if not(id and record):
        return {'perdido':'True'}
    else:
        appstruct = record_to_appstruct(record)
        if appstruct['nome'] == usuario:
            appstruct['e_o_proprio'] = True
        else:
            appstruct['e_o_proprio'] = False
        return appstruct
        #return {'form':form.render(appstruct=appstruct)}

@view_config(route_name='editar_perfil', renderer='editar_perfil.slim', permission='usar')
def editar_perfil(request):
    """Editar perfil de usuário"""
    dbsession = DBSession()
    nome = request.matchdict.get('nome')
    if nome:
        record = dbsession.query(BdUsuario).filter_by(nome=nome).first()
    if not(nome and record):
        return {'perdido':'True'}
    else:
        form = deform.Form(FormEditar(), buttons=('Alterar',))
        if 'Alterar' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())
            except deform.ValidationFailure, e:
                return {'form':e.render()}
            record = merge_session_with_post(record, appstruct.items())
            dbsession.merge(record)
            dbsession.flush()
            #return {'sucesso': 'True'}
            return HTTPFound(location=request.route_url('ver_perfil', id=nome))
        else:
            appstruct = record_to_appstruct(record)
        return {'form':form.render(appstruct=appstruct)}
        #return appstruct

@view_config(route_name='adicionar_automovel', renderer='registrar_carro.slim', permission='usar')
def adicionar_automovel(request):
    """Registro de carro"""
    dbsession = DBSession()
    nome = request.matchdict.get('nome')
    if nome:
        record = dbsession.query(BdUsuario).filter_by(nome=nome).first()
    if not(nome and record):
        return {'perdido':'True'}
    else:
        usu = record.nome
        form = deform.Form(FormAutomovel(), buttons=('Adicionar',))
        if 'Adicionar' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())
            except deform.ValidationFailure, e:
                return {'form':e.render()}
            dbsession = DBSession()

            atribs = request.POST
            atribs["usuario"] = usu

            record = BdAutomovel()
            record = merge_session_with_post(record, appstruct.items())
            record.usuario = usu
            dbsession.merge(record)
            dbsession.flush()
            return HTTPFound(location=request.route_url('listar_automoveis'))
        return {'form':form.render()}

@view_config(route_name='adicionar_rota', renderer='registrar_rota.slim', permission='usar')
def adicionar_rota(request):
    """Registro de rota"""
    dbsession = DBSession()
    nome = request.matchdict.get('nome')
    if nome:
        record = dbsession.query(BdUsuario).filter_by(nome=nome).first()
    if not(nome and record):
        return {'perdido':'True'}
    else:
        usu = record.nome
        form = deform.Form(FormRota(), buttons=('Adicionar',))
        if 'Adicionar' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())
            except deform.ValidationFailure, e:
                return {'form':e.render()}
            dbsession = DBSession()

            atribs = request.POST
            tratar_tempo(atribs)
            atribs["usuario"] = usu

            record = BdCarona()
            record = merge_session_with_post(record, appstruct.items())
            record.id_pais = 0
            record.usuario = usu
            dbsession.merge(record)
            dbsession.flush()
            return HTTPFound(location=request.route_url('listar_rotas'))
        return {'form':form.render()}

@view_config(route_name='listar_usuarios', renderer='listar.slim')
@view_config(route_name='listar_usuarios_busca', renderer='listar.slim')
def listar_usuarios(request):
    dbsession = DBSession()
    busca = request.matchdict.get('busca')
    if busca:
        busca = "%"+busca+"%"
        quer = dbsession.query(BdUsuario)
        usuarios = quer.filter(BdUsuario.nome.like(busca)).all()
    else:
        usuarios = dbsession.query(BdUsuario).all()

    form = deform.Form(FormBuscar(), buttons=('Buscar',))
    if 'Buscar' in request.POST:
        palavras = request.POST["busca"]
        url = request.route_url('listar_usuarios_busca',busca=palavras) 
        return HTTPFound(location=url)

    usuarios.sort(key=lambda u: u.nome)
    dicio = OrderedDict()
    for usuario in usuarios:
        dicio[usuario.nome] = usuario.nome
    return {'dicio':dicio,
            'link':"ver_perfil",
            'form': form.render(),
           }

@view_config(route_name='listar_rotas', renderer='listar.slim')
@view_config(route_name='listar_rotas_busca', renderer='listar.slim')
def listar_rotas(request):
    dbsession = DBSession()
    busca = request.matchdict.get('busca')
    if busca:
        busca = "%"+busca+"%"
        quer = dbsession.query(BdCarona)
        rotas = quer.filter(BdCarona.local_partida.like(busca)).all()
    else:
        rotas = dbsession.query(BdCarona).all()

    form = deform.Form(FormBuscar(), buttons=('Buscar',))
    if 'Buscar' in request.POST:
        palavras = request.POST["busca"]
        url = request.route_url('listar_rotas_busca',busca=palavras) 
        return HTTPFound(location=url)

    #usuarios.sort(key=lambda u: u.nome)
    dicio = OrderedDict()
    for rota in rotas:
        dicio[rota.id] = "%s -> %s" % (rota.local_partida, rota.local_chegada)
    return {'dicio':dicio,
            'link':"ver_rota",
            'form': form.render(),
           }

@view_config(route_name='listar_automoveis', renderer='listar.slim')
@view_config(route_name='listar_automoveis_busca', renderer='listar.slim')
def listar_automoveis(request):
    dbsession = DBSession()
    busca = request.matchdict.get('busca')
    if busca:
        busca = "%"+busca+"%"
        quer = dbsession.query(BdAutomovel)
        autos = quer.filter(BdAutomovel.cor.like(busca)).all()
    else:
        autos = dbsession.query(BdAutomovel).all()

    form = deform.Form(FormBuscar(), buttons=('Buscar',))
    if 'Buscar' in request.POST:
        palavras = request.POST["busca"]
        url = request.route_url('listar_automoveis_busca',busca=palavras) 
        return HTTPFound(location=url)

    #usuarios.sort(key=lambda u: u.nome)
    dicio = OrderedDict()
    for auto in autos:
        dicio[auto.id] = auto.cor
    return {'dicio':dicio,
            'link':"ver_automovel",
            'form': form.render(),
           }

@view_config(route_name='ver_rota', renderer='ver_rota.slim')
def ver_rota(request):
    """Ver uma rota"""
    usuario = authenticated_userid(request)
    dbsession = DBSession()
    id = request.matchdict.get('id')
    if id:
        record = dbsession.query(BdCarona).filter_by(id=id).first()
    if not(id and record):
        return {'perdido':'True'}
    else:
        appstruct = record_to_appstruct(record)
        if appstruct['usuario'] == usuario:
            e_o_proprio = True
        else:
            e_o_proprio = False
        if usuario not in record.adquiridos.split(','):
            pode_adquirir = True
        else:
            pode_adquirir = False
        return {
                'dados':appstruct,
                'e_o_proprio':e_o_proprio,
                'editar':"editar_rota",
                'pode_adquirir':pode_adquirir
                }

@view_config(route_name='ver_automovel', renderer='ver_auto.slim')
def ver_automovel(request):
    """Ver uma automovel"""
    usuario = authenticated_userid(request)
    dbsession = DBSession()
    id = request.matchdict.get('id')
    if id:
        record = dbsession.query(BdAutomovel).filter_by(id=id).first()
    if not(id and record):
        return {'perdido':'True'}
    else:
        appstruct = record_to_appstruct(record)
        if appstruct['usuario'] == usuario:
            e_o_proprio = True
        else:
            e_o_proprio = False
        return {
                'dicio':appstruct,
                'e_o_proprio':e_o_proprio,
                'editar':"editar_automovel",
                }

@view_config(route_name='editar_rota', renderer='editar_rotas.slim', permission='usar')
def editar_rota(request):
    """Editar rota de usuário"""
    dbsession = DBSession()
    id = request.matchdict.get('id')
    if id:
        record = dbsession.query(BdCarona).filter_by(id=id).first()
    if not(id and record):
        return {'perdido':'True'}
    else:
        form = deform.Form(FormRota(), buttons=('Alterar',))
        if 'Alterar' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())
            except deform.ValidationFailure, e:
                return {'form':e.render()}

            atribs = request.POST
            tratar_tempo(atribs)

            record = merge_session_with_post(record, appstruct.items())
            dbsession.merge(record)
            dbsession.flush()
            return HTTPFound(location=request.route_url('ver_rota', id=id))
        else:
            appstruct = record_to_appstruct(record)
        return {'form':form.render(appstruct=appstruct),
                'dados':appstruct,
               }

@view_config(route_name='editar_automovel', renderer='editar_autos.slim', permission='usar')
def editar_automovel(request):
    """Editar automovel de usuário"""
    dbsession = DBSession()
    id = request.matchdict.get('id')
    if id:
        record = dbsession.query(BdAutomovel).filter_by(id=id).first()
    if not(id and record):
        return {'perdido':'True'}
    else:
        form = deform.Form(FormAutomovel(), buttons=('Alterar',))
        if 'Alterar' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())
            except deform.ValidationFailure, e:
                return {'form':e.render()}
            record = merge_session_with_post(record, appstruct.items())
            dbsession.merge(record)
            dbsession.flush()
            return HTTPFound(location=request.route_url('ver_automovel', id=id))
        else:
            appstruct = record_to_appstruct(record)
        return {'form':form.render(appstruct=appstruct)}

@view_config(route_name='avaliar_usuario', permission='usar')
def avaliar(request):
    dbsession = DBSession()
    nome = request.matchdict.get('nome')
    nota = request.matchdict.get('nota')
    if nome:
        record = dbsession.query(BdUsuario).filter_by(nome=nome).first()
    if not(nome and record and nota):
        return HTTPFound(location=request.route_url('ver_perfil', id=nome))
    else:
        if nota == "bem":
            record.pontos_positivos += 1
        elif nota == "mal":
            record.pontos_negativos += 1
        return HTTPFound(location=request.route_url('ver_perfil', id=nome))

@view_config(route_name='adquirir_rota', permission='usar')
def adquirir(request):
    nome = authenticated_userid(request)
    dbsession = DBSession()
    id = request.matchdict.get('id')
    if id:
        record = dbsession.query(BdCarona).filter_by(id=id).first()
    if not(nome and record and id):
        return HTTPFound(location=request.route_url('ver_rota', id=id))
    else:
        if record.adquiridos:
            record.adquiridos += ","+nome
        else:
            record.adquiridos += nome
        return HTTPFound(location=request.route_url('ver_rota', id=id))

@view_config(route_name='bd_ler')
def bd_ler(request):
    dbsession = DBSession()
    nome = request.matchdict['nome']
    dicio = {"caronas": BdCarona,
             "usuarios": BdUsuario}
    lista = dbsession.query(dicio[nome]).all()
    rets = []
    for ret in lista:
        ret = record_to_appstruct(ret)
        for k in ret.keys():
            if isinstance(ret[k], date) or isinstance(ret[k], time):
                ret[k] = str(ret[k])
        rets.append(ret)

    return Response(json.dumps(rets))

@view_config(route_name='bd_alterar')
def bd_alterar(request):
    dbsession = DBSession()
    nome = request.matchdict['nome']
    dicio = {"caronas": BdCarona,
             "usuarios": BdUsuario}
    lista = dbsession.query(dicio[nome]).all()
    rets = []
    for ret in lista:
        ret = record_to_appstruct(ret)
        for k in ret.keys():
            if isinstance(ret[k], date) or isinstance(ret[k], time):
                ret[k] = str(ret[k])
        rets.append(ret)

    return Response(json.dumps(rets))

@view_config(route_name='bd_espelho')
def espelho(request):
    return Response(str(request))

@view_config(route_name='patrocinadores', renderer='patrocinadores.slim')
def patro(request):
    return {}
