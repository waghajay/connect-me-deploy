import os
import django
from django.core.asgi import get_asgi_application

def configure_django_settings():
    # Set the DJANGO_SETTINGS_MODULE environment variable
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ConnectMe.settings")

    # Initialize Django settings
    django.setup()

if __name__ == "__main__":
    # Call the function to configure Django settings
    configure_django_settings()

    # Get the ASGI application
    application = get_asgi_application()

    # Now you can run Daphne with the configured ASGI application
    import sys
    from daphne.cli import CommandLineInterface

    sys.argv[0] = "daphne"
    sys.exit(CommandLineInterface.entrypoint())
