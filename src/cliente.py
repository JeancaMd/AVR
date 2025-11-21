# src/cliente.py
import socket

class ControladorUDP:
    """
    Cliente UDP que se registra ante el Pico y escucha paquetes entrantes.
    Uso:
        c = ControladorUDP(pico_ip="192.168.0.105", pico_port=5000)
        comando = c.obtener_evento()  # None o string con el comando
    """
    def __init__(self, pico_ip="192.168.0.105", pico_port=5000, timeout=0.02):
        self.pico_addr = (pico_ip, pico_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # no bind explícito: usamos puerto efímero del sistema para enviar/recibir
        self.sock.settimeout(timeout)
        # enviar mensaje inicial para que el Pico registre nuestra dirección
        try:
            self.sock.sendto(b"hola_pico", self.pico_addr)
        except Exception as e:
            print("ControladorUDP: error enviando registro:", e)

    def obtener_evento(self):
        """Devuelve el comando recibido desde el Pico (str) o None si no hay nada."""
        try:
            data, addr = self.sock.recvfrom(1024)
            if not data:
                return None
            comando = data.decode().strip()
            return comando
        except socket.timeout:
            return None
        except OSError:
            return None
        except Exception as e:
            # no interrumpir el juego por un error de socket
            print("ControladorUDP recibir error:", e)
            return None
