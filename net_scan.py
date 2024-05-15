import argparse
import subprocess
import os

def scan_network(router_ip):
    try:
        # Ejecuta el comando nmap a través de Termux para escanear la red
        result = subprocess.run(['nmap', '-sn', f'{router_ip}/24'], capture_output=True, text=True)

        # Analiza la salida del comando nmap para extraer las direcciones IP de los dispositivos
        lines = result.stdout.split('\n')
        devices = []
        for line in lines:
            if 'Nmap scan report for' in line:
                parts = line.split()
                ip_address = parts[4]
                devices.append(ip_address)

        return devices

    except Exception as e:
        return str(e)

def save_ips_to_file(ips):
    try:
        # Verifica si la carpeta Downloads existe, si no, la crea
        downloads_folder = os.path.join(os.environ['EXTERNAL_STORAGE'], 'Download')
        if not os.path.exists(downloads_folder):
            os.mkdir(downloads_folder)

        # Escribe las direcciones IP en un archivo .txt en la carpeta Downloads
        file_path = os.path.join(downloads_folder, 'ips.txt')
        with open(file_path, 'w') as file:
            for ip in ips:
                file.write(ip + '\n')

        print(f'Las direcciones IP se han guardado en {file_path}')
    except Exception as e:
        print('Error al guardar las direcciones IP:', str(e))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network Scanner')
    parser.add_argument('--router', '-r', type=str, required=True, help='Router IP address')
    args = parser.parse_args()

    devices = scan_network(args.router)
    if isinstance(devices, list):
        print('Dispositivos conectados en la red:')
        for device in devices:
            print(device)

        save_to_file = input('¿Deseas guardar las direcciones IP en un archivo? (y/n): ')
        if save_to_file.lower() == 'y':
            save_ips_to_file(devices)
    else:
        print('Error:', devices)

