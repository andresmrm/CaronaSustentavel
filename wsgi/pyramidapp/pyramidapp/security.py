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
