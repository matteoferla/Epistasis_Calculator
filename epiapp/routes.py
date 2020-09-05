def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('api', '/api')
    config.add_route('download', '/download')
    config.add_route('create', '/create')
    config.add_route('demo', '/demo')
