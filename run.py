import subprocess
from subprocess import CompletedProcess
import os

# Ejecutar el script para actualizar el archivo .env con la IP pública
process1: CompletedProcess = subprocess.run(["python", "app/update_ip.py"])

# Arrancar el servidor uvicorn
if process1.returncode == 0: 
    subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"])
