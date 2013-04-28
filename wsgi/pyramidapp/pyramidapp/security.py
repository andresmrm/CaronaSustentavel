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

import time

from .models import (
    DBSession,
    BdUsuario,
)

CACHE = {}


def groupfinder(nome, request):
    tempo = CACHE.get(nome)
    if not tempo or (time.time()-tempo) > 60:
        dbsession = DBSession()
        jog = dbsession.query(BdUsuario).filter_by(nome=nome).first()
        CACHE[nome] = time.time()
    else:
        jog = True
    if jog:
        return ['g:usuario']
        #return ['g:%s' % g for g in jog.groups]
