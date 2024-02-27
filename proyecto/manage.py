#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import sys

import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto.settings")

    from django.core.management import execute_from_command_line

    # Verifica si el puerto está disponible
    port = 8002  # Cambia a tu puerto deseado
    try:
        from django.core.servers.basehttp import run
        run(port=int(port))
    except Exception as e:
        print(f"Error al intentar ejecutar en el puerto {port}: {e}")
        print(f"Intentando en el puerto siguiente...")
        port += 1
        run(port=int(port))
