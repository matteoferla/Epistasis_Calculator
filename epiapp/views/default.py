from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/epistasis.mako')
def epi(request):  # serving static basically.
    return {}
