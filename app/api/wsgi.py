"""
WSGI config for api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os


#####################################################################################
# Remote Debug configuration
#####################################################################################

# The debugpy.listen() function starts a new debugging session and waits for a client to attach to it.
# The debugpy.wait_for_client() function blocks the execution of the program until a client is attached to the debugging session.
# The debugpy.breakpoint() function can be used to set a breakpoint in the code.
# The debugpy.log_to() function can be used to log messages to a file.

# ! Enable or Disable the remote debugging.
if False:
    import debugpy # ! this needs to be manually installed "pip install debugpy" in the development environment.

    # Disabilita il caricamento della libreria nativa di pydevd
    os.environ['PYDEVD_LOAD_NATIVE_LIB'] = '0'

    #import logging
    #logging.basicConfig(level=logging.DEBUG)
    #logger = logging.getLogger()
    #debugpy.log_to("/var/log/automation/debugpy")

    debugpy.listen(('0.0.0.0', 5678))
    print("⚠️ Debug server is waiting for a connection on 5678")
    debugpy.wait_for_client()  # Wait for the debugger client to attach

#####################################################################################


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

application = get_wsgi_application()

