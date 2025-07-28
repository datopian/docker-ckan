#!/usr/bin/env python

import os

# get site title from CKAN env
SITENAME = (os.environ.get('CKAN_SITE_TITLE') or
            os.environ.get('CKAN__SITE_TITLE'))

# Check whether we are in maintenance mode or not
MAINTENANCE = os.environ.get('MAINTENANCE_MODE', '')

# template data variables
# - NAME: CKAN instance name
MAINTENANCE_TPL = """
<html>
    <head>
        <title>%(NAME)s Maintenance</title>
    </head>
    <body>
            <h1>Maintenance mode</h1>
            <p>%(NAME)s is currently under maintenance. We'll be back online
            soon, apologies for the inconvenience.</p>
    </body>
</html>
"""

maintenance_data = {
    'NAME': SITENAME,
}

if (MAINTENANCE.lower() == 'true'):
    def application(environ, start_response):
        status = '503 Service Unavailable'
        output = (MAINTENANCE_TPL % maintenance_data)
        response_headers = [('Content-type', 'text/html'),
                            ('Content-Length', str(len(output)))]

        start_response(status, response_headers)

        return [output]
else:
    from paste.deploy import loadapp

    config_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'ckan.ini')
    from paste.script.util.logging_config import fileConfig
    fileConfig(config_filepath)
    application = loadapp('config:%s' % config_filepath)
