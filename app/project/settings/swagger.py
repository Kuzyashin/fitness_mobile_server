# -*- coding: utf-8 -*-
SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '0.1',
    'api_path': '/api',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': False,
    'is_superuser': False,
    'permission_denied_handler': None,
    'resource_access_handler': None,
    'base_path': '127.0.0.1:8000/docs',
    'info': {
        'contact': '',
        'description':
            'This is a sample server for testing RESTful APIs.'
            'All API endpoints return fake information for testing needs.'
            ,
        'license': 'Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'title': 'Base Django Project',
    },
    'doc_expansion': 'none',
}