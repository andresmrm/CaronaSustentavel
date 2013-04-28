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

from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget, authenticated_userid
#from sqlalchemy import DBAPIError
import deform

from .models import (
    DBSession,
    BdUsuario,
    )

from forms import *



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
    return {"usuario":usuario}


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
        record = merge_session_with_post(record, request.POST.items())
        dbsession.merge(record)
        dbsession.flush()
        return {'sucesso': 'True'}
    return {'form':form.render()}

@view_config(route_name='ver_perfil', renderer='ver_perfil.slim')
def ver_perfil(request):
    """Ver perfil de usuário"""
    usuario = authenticated_userid(request)
    dbsession = DBSession()
    record = dbsession.query(BdUsuario).filter_by(nome=request.matchdict['nome']).first()
    if record == None:
        return {'perdido':'True'}
    else:
        appstruct = record_to_appstruct(record)
        if appstruct['nome'] == usuario:
            appstruct['e_o_proprio'] = True
        return appstruct
        #return {'form':form.render(appstruct=appstruct)}

@view_config(route_name='editar_perfil', renderer='editar_perfil.slim', permission='usar')
def editar_perfil(request):
    """Editar perfil de usuário"""
    dbsession = DBSession()
    record = dbsession.query(BdUsuario).filter_by(nome=request.matchdict['nome']).first()
    if record == None:
        return {'perdido':'True'}
    else:
        form = deform.Form(FormEditar(), buttons=('Alterar',))
        if 'Alterar' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())
            except deform.ValidationFailure, e:
                return {'form':e.render()}
            record = merge_session_with_post(record, request.POST.items())
            dbsession.merge(record)
            dbsession.flush()
            return {'sucesso': 'True'}
        else:
            appstruct = record_to_appstruct(record)
        return {'form':form.render(appstruct=appstruct)}

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
