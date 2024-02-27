#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Verifica si el comando 'runserver' se proporciona y si no, usa el puerto predeterminado 8000
    if 'runserver' in sys.argv and '--port' not in sys.argv:
        sys.argv += ['--', '8002']  # Puedes cambiar '8001' al puerto que desees
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
