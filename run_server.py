from waitress import serve
from PuntoVenta.wsgi import application
import socket

def obtener_ip_real():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

ip_address = obtener_ip_real()

print("-----------------------------------------------------")
print(" SISTEMA PUNTO DE VENTA - EN LÍNEA (MODO PRODUCCIÓN)")
print("-----------------------------------------------------")
print(f" > Acceso local:   http://localhost:8080")
print(f" > Acceso en Red:  http://{ip_address}:8080")
print("-----------------------------------------------------")
print(" EL SERVIDOR ESTÁ CORRIENDO. NO CIERRES ESTA VENTANA.")

serve(application, host='0.0.0.0', port=8080, threads=4)