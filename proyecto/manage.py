import os
import sys
import socket
from random import randint

def get_free_port():
    port = None
    while True:
        random_port = randint(8000, 9000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", random_port))
                port = random_port
                return port
            except:
                pass
                
def main():
    port = get_free_port() 
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

    try:
        from django.core.management import execute_from_command_line  
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django..."
        ) from exc
            
    print(f"Corriendo en puerto {port}") 

    execute_from_command_line([
        sys.argv[0], 
        "runserver", 
        f"127.0.0.1:{port}"
    ])

if __name__ == '__main__':
    main()