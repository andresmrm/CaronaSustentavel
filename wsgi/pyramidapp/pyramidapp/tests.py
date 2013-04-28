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

import unittest
import transaction

from pyramid import testing

from .models import DBSession


class TestMyView(unittest.TestCase):
    def setUp(self):
        pass
        #self.config = testing.setUp()
        #from sqlalchemy import create_engine
        #engine = create_engine('sqlite://')
        #from .models import (
        #    Base,
        #    MyModel,
        #    )
        #DBSession.configure(bind=engine)
        #Base.metadata.create_all(engine)
        #with transaction.manager:
        #    model = MyModel(name='one', value=55)
        #    DBSession.add(model)

    def tearDown(self):
        pass
        #DBSession.remove()
        #testing.tearDown()

    def test_it(self):
        pass
        #from .views import my_view
        #request = testing.DummyRequest()
        #info = my_view(request)
        #self.assertEqual(info['one'].name, 'one')
        #self.assertEqual(info['project'], 'projeto')
