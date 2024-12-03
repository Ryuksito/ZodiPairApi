import os
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener la IP pública actual (puedes usar cualquier servicio que prefieras)
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        return response.text.strip()  # Devuelve la IP pública
    except requests.RequestException:
        return None  # Si no se puede obtener la IP

# Actualizar la variable IP en el archivo .env
def update_env_file(public_ip):
    dotenv_path = 'app/.env'  # Ruta al archivo .env
    if public_ip:
        # Leer el archivo .env existente
        with open(dotenv_path, 'r') as file:
            lines = file.readlines()

        # Buscar y actualizar la variable IP
        with open(dotenv_path, 'w') as file:
            for line in lines:
                if line.startswith("IP="):
                    file.write(f"IP={public_ip}\n")
                else:
                    file.write(line)

def update_env_file_local():
    dotenv_path = 'app/.env'  # Ruta al archivo .env
    # Leer el archivo .env existente
    with open(dotenv_path, 'r') as file:
        lines = file.readlines()

    # Buscar y actualizar la variable IP
    with open(dotenv_path, 'w') as file:
        for line in lines:
            if line.startswith("IP="):
                file.write(f"IP=127.0.0.1\n")
            else:
                file.write(line)

if __name__ == "__main__":
    
    opt = int(input("Run for: \n1)- Dev Mode\n2)- Deploy Mode\n"))

    if opt == 1:
        update_env_file_local()
    elif opt == 2:
        # Obtener la IP pública
        public_ip = get_public_ip()

        if public_ip:
            print(f"IP pública detectada: {public_ip}")
            # Actualizar el archivo .env con la IP obtenida
            update_env_file(public_ip)
        else:
            print("No se pudo obtener la IP pública. Usando IP por defecto.")
    else: raise Exception("bad option choosen")

