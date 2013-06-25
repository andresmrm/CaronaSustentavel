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


class MyTest(unittest.TestCase):
    def setUp(self):
        #self.config = testing.setUp()
        request = testing.DummyRequest()
        self.config = testing.setUp(request=request)
        transaction.begin()

    def tearDown(self):
        testing.tearDown()
        transaction.abort()

    def test_incial1(self):
        resp = criar_perfil(get_current_request())
        self.assertEqual(resp.keys()[0], "form")
        self.assertTrue(resp.values()[0].count("form"))

    def test_incial2(self):
        request = get_current_request()
        request.POST["Registrar"] = "Registrar"
        resp = criar_perfil(request)
        self.assertEqual(resp.keys()[0], "form")
        self.assertTrue(resp.values()[0].count("form"))

    def test_incial3(self):
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
        self.assertEqual(resp.keys()[0], "perdido")

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
        self.assertEqual(resp.keys()[0], "form")
        self.assertTrue(resp.values()[0].count("form"))
