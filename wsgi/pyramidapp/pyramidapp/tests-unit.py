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

from datetime import date
import unittest
from pyramid import testing
from pyramid.threadlocal import get_current_request
from paste.util.multidict import MultiDict

from sqlalchemy import create_engine
from .models import *
import transaction

from pyramid.httpexceptions import HTTPFound

from views import *


def setUpModule():
    # once for all the tests in this module:
 
    # create an engine bound to the test db
    engine = create_engine('sqlite:///test.db')
 
    # first use of DBSession, bind it to our engine
    DBSession.configure(bind=engine)
 
    # bind our engine to the metadata so we can call drop_all later without
    # having the engine around
    Base.metadata.bind = engine
 
    # create_all to create tables
    Base.metadata.create_all()

def tearDownModule():
    Base.metadata.drop_all()


class TestesPerfil(unittest.TestCase):
    def setUp(self):
        request = testing.DummyRequest()
        self.config = testing.setUp(request=request)
        transaction.begin()

    def tearDown(self):
        testing.tearDown()
        transaction.abort()

    def test_criar_perfil1(self):
        resp = criar_perfil(get_current_request())
        self.assertNotEqual(resp.get('form'), None)
        self.assertTrue(resp['form'].count("form"))

    def test_criar_perfil2(self):
        request = get_current_request()
        request.POST["Registrar"] = "Registrar"
        resp = criar_perfil(request)
        self.assertNotEqual(resp.get('form'), None)
        self.assertTrue(resp['form'].count("form"))

    def test_criar_perfil3(self):
        request = get_current_request()
        request.POST = MultiDict()
        for a,b in [('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('nome', u'test2'), ('__start__', u'senha:mapping'), ('senha', u'11111'), ('senha-confirm', u'11111'), ('__end__', u'senha:mapping'), ('email', u'a@a.com'), ('cidade', u'a'), ('estado', u'aa'), ('pais', u'a'), ('cep', u'1'), ('idade', u'1'), ('celular', u'1'), ('ano_habilitacao', u'1'), ('altura', u'1'), ('peso', u'1'), ('cachorro', u'true'), ('Registrar', u'Registrar')]:
            request.POST[a] = b
        self.config.add_route('login', '/login')
        resp = criar_perfil(request)
        self.assertIsInstance(resp, HTTPFound)

    def test_ver_perfil1(self):
        request = get_current_request()
        resp = ver_perfil(request)
        self.assertEqual(resp.keys()[0], "perdido")

    def test_ver_perfil2(self):
        request = get_current_request()
        request.matchdict["id"] = "a"
        dbsession = DBSession()
        record = BdUsuario("a","12345","a@a.com","1","1","1","1","1","1",False,True,False,date.today(),"a","aa","a")
        dbsession.merge(record)
        dbsession.flush()
        resp = ver_perfil(request)
        self.assertEqual(resp["e_o_proprio"], False)

    def test_ver_perfil3(self):
        self.config.testing_securitypolicy(userid='a', permissive=False)
        request = get_current_request()
        request.matchdict["id"] = "a"
        dbsession = DBSession()
        record = BdUsuario("a","12345","a@a.com","1","1","1","1","1","1",False,True,False,date.today(),"a","aa","a")
        dbsession.merge(record)
        dbsession.flush()
        resp = ver_perfil(request)
        self.assertEqual(resp["e_o_proprio"], True)


    def test_editar_perfil1(self):
        request = get_current_request()
        resp = editar_perfil(request)
        self.assertNotEqual(resp.get('perdido'), None)

    def test_editar_perfil2(self):
        self.config.testing_securitypolicy(userid='a', permissive=True)
        dbsession = DBSession()
        record = BdUsuario("a","12345","a@a.com","1","1","1","1","1","1",False,True,False,date.today(),"a","aa","a")
        dbsession.merge(record)
        dbsession.flush()
        request = get_current_request()
        request.matchdict["nome"] = "a"
        request.POST = MultiDict()
        for a,b in [('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('__start__', u'senha:mapping'), ('senha', u'11111'), ('senha-confirm', u'11111'), ('__end__', u'senha:mapping'), ('email', u'a@a.com'), ('cidade', u'a'), ('estado', u'aa'), ('pais', u'a'), ('cep', u'1'), ('idade', u'1'), ('celular', u'1'), ('ano_habilitacao', u'1'), ('altura', u'1'), ('peso', u'1'), ('cachorro', u'true'), ('Alterar', u'Alterar')]:
            request.POST[a] = b
        self.config.add_route('ver_perfil', '/{id}')
        resp = editar_perfil(request)
        self.assertIsInstance(resp, HTTPFound)

    def test_editar_perfil3(self):
        self.config.testing_securitypolicy(userid='a', permissive=True)
        dbsession = DBSession()
        record = BdUsuario("a","12345","a@a.com","1","1","1","1","1","1",False,True,False,date.today(),"a","aa","a")
        dbsession.merge(record)
        dbsession.flush()
        request = get_current_request()
        request.matchdict["nome"] = "a"
        request.POST = MultiDict()
        for a,b in [('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('__start__', u'senha:mapping'), ('senha', u''), ('senha-confirm', u'11111'), ('__end__', u'senha:mapping'), ('email', u'a@a.com'), ('cidade', u'a'), ('estado', u'aa'), ('pais', u'a'), ('cep', u'1'), ('idade', u'1'), ('celular', u'1'), ('ano_habilitacao', u'1'), ('altura', u'1'), ('peso', u'1'), ('cachorro', u'true'), ('Alterar', u'Alterar')]:
            request.POST[a] = b
        resp = editar_perfil(request)
        self.assertNotEqual(resp.get('form'), None)
        self.assertTrue(resp['form'].count("form"))


class TestesAdicionar(unittest.TestCase):
    def setUp(self):
        request = testing.DummyRequest()
        self.config = testing.setUp(request=request)
        transaction.begin()
        record = BdUsuario("a","12345","a@a.com","1","1","1","1","1","1",False,True,False,date.today(),"a","aa","a")
        dbsession = DBSession()
        dbsession.merge(record)
        dbsession.flush()

    def tearDown(self):
        testing.tearDown()
        transaction.abort()

    def test_adicionar_automovel1(self):
        resp = adicionar_automovel(get_current_request())
        self.assertEqual(resp.keys()[0], "perdido")

    def test_adicionar_automovel2(self):
        self.config.testing_securitypolicy(userid='a', permissive=True)
        request = get_current_request()
        request.matchdict["nome"] = "a"
        request.POST = MultiDict()
        for a,b in [('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('cor', u'qwwqe'), ('ano', u'11111'), ('placa', u'111'), ('nro_assentos', u'1111'), ('Adicionar', u'Adicionar')]:
            request.POST[a] = b
        self.config.add_route('listar_automoveis', '/')
        resp = adicionar_automovel(request)
        self.assertIsInstance(resp, HTTPFound)

    def test_adicionar_automovel3(self):
        self.config.testing_securitypolicy(userid='a', permissive=True)
        request = get_current_request()
        request.matchdict["nome"] = "a"
        request.POST = MultiDict()
        for a,b in [('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('cor', u'qwwqe'), ('ano', u'11111'), ('placa', u'111'), ('nro_assentos', u'aaaa'), ('Adicionar', u'Adicionar')]:
            request.POST[a] = b
        resp = adicionar_automovel(request)
        self.assertNotEqual(resp.get('form'), None)
        self.assertTrue(resp['form'].count("form"))

    def test_adicionar_rota1(self):
        resp = adicionar_rota(get_current_request())
        self.assertEqual(resp.keys()[0], "perdido")

    def test_adicionar_rota2(self):
        self.config.testing_securitypolicy(userid='a', permissive=True)
        request = get_current_request()
        request.matchdict["nome"] = "a"
        request.POST = MultiDict()
        for a,b in [('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('local_partida', u'Sao Paulo'), ('local_chegada', u'Diadema'), ('data_partida', u'1'), ('data_chegada', u'1'), ('hora_partida', u'1'), ('hora_chegada', u'1'), ('frequencia', u'1'), ('possibilidade_desvio', u'1'), ('tolerancia_atraso', u'1'), ('custo', u'2'), ('Adicionar', u'Adicionar')]:
            request.POST[a] = b
        self.config.add_route('listar_rotas', '/')
        resp = adicionar_rota(request)
        self.assertIsInstance(resp, HTTPFound)

    def test_adicionar_rota3(self):
        self.config.testing_securitypolicy(userid='a', permissive=True)
        request = get_current_request()
        request.matchdict["nome"] = "a"
        request.POST = MultiDict()
        for a,b in [('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('_charset_', u'UTF-8'), ('__formid__', u'deform'), ('local_partida', u'Sao Paulo'), ('local_chegada', u''), ('data_partida', u'1'), ('data_chegada', u'1'), ('hora_partida', u'1'), ('hora_chegada', u'1'), ('frequencia', u'1'), ('possibilidade_desvio', u'1'), ('tolerancia_atraso', u'1'), ('Adicionar', u'Adicionar')]:
            request.POST[a] = b
        resp = adicionar_rota(request)
        self.assertEqual(resp.keys()[0], "form")
        self.assertTrue(resp.values()[0].count("form"))


class TestesListar(unittest.TestCase):
    def setUp(self):
        request = testing.DummyRequest()
        self.config = testing.setUp(request=request)
        transaction.begin()

    def tearDown(self):
        testing.tearDown()
        transaction.abort()

    def test_listar_usuarios1(self):
        resp = listar_usuarios(get_current_request())
        self.assertEqual(len(resp["dicio"]), 0)
        self.assertTrue(resp["form"].count("form"))

    def test_listar_usuarios2(self):
        record = BdUsuario("a","12345","a@a.com","1","1","1","1","1","1",False,True,False,date.today(),"a","aa","a")
        dbsession = DBSession()
        dbsession.merge(record)
        dbsession.flush()
        resp = listar_usuarios(get_current_request())
        self.assertEqual(len(resp["dicio"]), 1)
        self.assertTrue(resp["form"].count("form"))

    def test_listar_rotas1(self):
        resp = listar_rotas(get_current_request())
        self.assertEqual(len(resp["dicio"]), 0)
        self.assertTrue(resp["form"].count("form"))

    def test_listar_rotas2(self):
        record = BdUsuario("a","12345","a@a.com","1","1","1","1","1","1",False,True,False,date.today(),"a","aa","a")
        dbsession = DBSession()
        dbsession.merge(record)
        record = BdCarona("a","12345","a@a.com","1","1","1","1","1","1","a","aa")
        dbsession = DBSession()
        dbsession.merge(record)
        dbsession.flush()
        resp = listar_rotas(get_current_request())
        self.assertEqual(len(resp["dicio"]), 1)
        self.assertTrue(resp["form"].count("form"))

    def test_listar_automoveis1(self):
        resp = listar_automoveis(get_current_request())
        self.assertEqual(len(resp["dicio"]), 0)
        self.assertTrue(resp["form"].count("form"))

    def test_listar_automoveis2(self):
        record = BdUsuario("a","12345","a@a.com","1","1","1","1","1","1",False,True,False,date.today(),"a","aa","a")
        dbsession = DBSession()
        dbsession.merge(record)
        record = BdAutomovel("a","12345","a@a.com","1","1","1")
        dbsession.merge(record)
        dbsession.flush()
        resp = listar_automoveis(get_current_request())
        self.assertEqual(len(resp["dicio"]), 1)
        self.assertTrue(resp["form"].count("form"))

class TestesVer(unittest.TestCase):
    def setUp(self):
        request = testing.DummyRequest()
        self.config = testing.setUp(request=request)
        transaction.begin()
        dbsession = DBSession()
        record = BdUsuario("a","12345","a@a.com","1","1","1","1","1","1",False,True,False,date.today(),"a","aa","a")
        dbsession.merge(record)
        record = BdCarona("a","12345","a@a.com","1","1","1","1","1","1","a","aa")
        dbsession.merge(record)
        record = BdAutomovel("a","12345","a@a.com","1","1","1")
        dbsession.merge(record)
        dbsession.flush()

    def tearDown(self):
        testing.tearDown()
        transaction.abort()

    def test_ver_rota1(self):
        request = get_current_request()
        resp = ver_rota(request)
        self.assertEqual(resp.keys()[0], "perdido")

    def test_ver_rota2(self):
        request = get_current_request()
        request.matchdict["id"] = "1"
        resp = ver_rota(request)
        self.assertEqual(resp["e_o_proprio"], False)

    def test_ver_rota3(self):
        self.config.testing_securitypolicy(userid='a', permissive=False)
        request = get_current_request()
        request.matchdict["id"] = "1"
        resp = ver_rota(request)
        self.assertEqual(resp["e_o_proprio"], True)

    def test_ver_automovel1(self):
        request = get_current_request()
        resp = ver_automovel(request)
        self.assertEqual(resp.keys()[0], "perdido")

    def test_ver_automovel2(self):
        request = get_current_request()
        request.matchdict["id"] = "1"
        resp = ver_automovel(request)
        self.assertEqual(resp["e_o_proprio"], False)

    def test_ver_automovel3(self):
        self.config.testing_securitypolicy(userid='a', permissive=False)
        request = get_current_request()
        request.matchdict["id"] = "1"
        resp = ver_automovel(request)
        self.assertEqual(resp["e_o_proprio"], True)

class TestesEditar(unittest.TestCase):
    def setUp(self):
        request = testing.DummyRequest()
        self.config = testing.setUp(request=request)
        transaction.begin()
        record = BdUsuario("a","12345","a@a.com","1","1","1","1","1","1",False,True,False,date.today(),"a","aa","a")
        dbsession = DBSession()
        dbsession.merge(record)
        dbsession.flush()

    def tearDown(self):
        testing.tearDown()
        transaction.abort()

