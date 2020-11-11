from pyramid.view import view_config

@view_config(route_name='docs', renderer='../templates/docs.mako')
def docs(request):
    return {}