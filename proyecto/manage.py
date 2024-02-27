import os
import socket
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto.settings")

    from django.core.management import execute_from_command_line

    # Intenta encontrar un puerto disponible a partir de 8002
    port = 8002
    while True:
        try:
            # Intenta abrir un socket en el puerto actual
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
            break  # Si tiene éxito, sal de bucle
        except OSError:
            print(f"El puerto {port} está en uso. Intentando el siguiente puerto...")
            port += 1

    print(f"Ejecutando en el puerto {port}")
    execute_from_command_line([sys.argv[0], "runserver", f"127.0.0.1:{port}"])
