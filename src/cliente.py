import socket

class ControladorUDP:
    def __init__(self, pico_ip="192.168.0.100", pico_port=5000, timeout=0.02):
        self.pico_addr = (pico_ip, pico_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        try:
            self.sock.sendto(b"Cliente conectado", self.pico_addr)
        except Exception as e:
            print("ControladorUDP: error enviando registro:", e)
        ### Evitar multiples clicks
        self.ultimo_comando = None

    def obtener_evento(self):
        try:
            data, addr = self.sock.recvfrom(1024)
            if not data:
                return None
            comando = data.decode().strip()

            if comando == self.ultimo_comando:
                return None 
            self.ultimo_comando = comando
            return comando
        except socket.timeout:
            self.ultimo_comando = None
            return None
        except OSError:
            return None
        except Exception as e:
            print("ControladorUDP recibir error:", e)
            return None

