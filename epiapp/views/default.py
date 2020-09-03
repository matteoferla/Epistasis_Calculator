from pyramid.view import view_config

import logging

log = logging.getLogger(__name__)

@view_config(route_name='home', renderer='../templates/epistasis.mako')
def epi(request):  # serving static basically.
    log.info('Serving main page')
    return {}
