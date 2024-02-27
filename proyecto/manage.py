import os
import socket 
import sys

port = os.environ.get("PORT", 8085)

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto.settings")
    
    from django.core.management import execute_from_command_line
    
    print(f"Ejecutando en el puerto {port}")
    
    execute_from_command_line([
        sys.argv[0], 
        "runserver", 
        f"{socket.gethostname()}:{port}"
    ])