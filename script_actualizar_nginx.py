import os
import requests

# Función para obtener la IP pública
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        return response.text.strip()
    except requests.RequestException:
        return None

# Función para actualizar el archivo de configuración de NGINX
def update_nginx_config(public_ip):
    nginx_config_path = '/etc/nginx/sites-available/zodipairapi'  # Ruta al archivo de configuración de NGINX
    
    if public_ip:
        # Leer el archivo de configuración de NGINX
        with open(nginx_config_path, 'r') as file:
            lines = file.readlines()

        # Buscar y actualizar la línea de server_name con la IP pública
        with open(nginx_config_path, 'w') as file:
            for line in lines:
                if line.startswith("server_name"):
                    file.write(f"server_name {public_ip};\n")  # Reemplazamos la IP local por la pública
                else:
                    file.write(line)
        print(f"Archivo de configuración de NGINX actualizado con la IP pública: {public_ip}")
    else:
        print("No se pudo obtener la IP pública.")

# Función para recargar NGINX y aplicar los cambios
def reload_nginx():
    os.system("sudo systemctl reload nginx")
    print("NGINX recargado para aplicar los cambios.")

if __name__ == "__main__":
    # Obtener la IP pública
    public_ip = get_public_ip()

    if public_ip:
        print(f"IP pública detectada: {public_ip}")
        # Actualizar la configuración de NGINX
        update_nginx_config(public_ip)
        # Recargar NGINX
        reload_nginx()
    else:
        print("No se pudo obtener la IP pública.")
