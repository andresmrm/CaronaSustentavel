import os

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from security import groupfinder


from .models import (
    DBSession,
    Base,
    UserFactory,
    initialize_sql
)

#from pyramidapp.models import appmaker


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # OpenShift Settings
    if os.environ.get('OPENSHIFT_DB_URL'):
        settings['sqlalchemy.url'] = \
            '%(OPENSHIFT_DB_URL)s%(OPENSHIFT_APP_NAME)s' % os.environ
    engine = engine_from_config(settings, 'sqlalchemy.')
    #get_root = appmaker(engine)
    #config = Configurator(settings=settings, root_factory=get_root)

    initialize_sql(engine)
    root_fac = '.models.RootFactory'
    config = Configurator(settings=settings, root_factory=root_fac)
    config.add_static_view('static', 'pyramidapp:static')
    #config.add_static_view('static', 'static', cache_max_age=3600)

    key = 'F#%$HG$JG#%$JHG#$UG$#NV#THFG$GF$FW[]{#F#F},.<#>$FM#MdwDCREF%$gfe'
    authn_policy = AuthTktAuthenticationPolicy(key, callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('deform_static', 'deform:static')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('criar_perfil', '/registrar')
    config.add_route('ver_perfil', '/ver_perfil/{id}')
    config.add_route('editar_perfil', '/editar_perfil/{nome}',
                     factory=UserFactory, traverse="/{nome}")
    config.add_route('listar_usuarios', '/lista_usuarios')

    config.add_route('adicionar_automovel', '/adicionar_automovel/{nome}')
    config.add_route('ver_automovel', '/ver_automovel/{id}')
    config.add_route('editar_automovel', '/editar_automovel/{id}')
    config.add_route('listar_automoveis', '/lista_automoveis')

    config.add_route('adicionar_rota', '/adicionar_rota/{nome}')
    config.add_route('ver_rota', '/ver_rota/{id}')
    config.add_route('editar_rota', '/editar_rota/{id}')
    config.add_route('listar_rotas', '/lista_rotas')

    config.add_route('inicial', '/')
    config.scan()
    return config.make_wsgi_app()
