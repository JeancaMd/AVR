from machine import Pin, ADC
from time import sleep
import network, usocket, time

# Conexión WiFi
red = network.WLAN(network.STA_IF)
red.active(True)
red.ifconfig((
    "192.168.0.100",   
    "255.255.255.0", 
    "192.168.1.1",    
    "8.8.8.8"         
))
red.connect("Carlos Quiros_EXT", "kristy1959")

print("Conectando a WIFI...")
while not red.isconnected():
    time.sleep(1)
print("WiFi conectado:", red.ifconfig())

# Servidor UDP
socket_servidor = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
socket_servidor.bind((red.ifconfig()[0], 5000))
socket_servidor.settimeout(0.1)
print("Servidor UDP activo en:", red.ifconfig()[0])

# Joystick y botones
x_pin = ADC(26)
y_pin = ADC(27)
sw_pin = Pin(22, Pin.IN, Pin.PULL_UP)
led = Pin(17, Pin.OUT)

btn_square = Pin(15, Pin.IN, Pin.PULL_UP)
btn_triangle = Pin(10, Pin.IN, Pin.PULL_UP)
btn_x = Pin(6, Pin.IN, Pin.PULL_UP)
btn_o = Pin(2, Pin.IN, Pin.PULL_UP)

direccion_cliente = None

def enviar(msg):
    if direccion_cliente:
        socket_servidor.sendto(msg.encode(), direccion_cliente)

# Estados previos
prev_sw = 1
prev_sq = 1
prev_tri = 1
prev_xbtn = 1
prev_obtn = 1
prev_y = 32768  # valor medio ADC
prev_x = 32768

while True:
    x_val = x_pin.read_u16()
    y_val = y_pin.read_u16()

    sw_val = sw_pin.value()
    sq_val = btn_square.value()
    tri_val = btn_triangle.value()
    xbtn_val = btn_x.value()
    obtn_val = btn_o.value()

    evento = False

    # --- Joystick presionado ---
    if sw_val == 0 and prev_sw == 1:
        evento = True
        print("Joystick presionado")
        enviar("JOYSTICK_PRESIONADO")
    prev_sw = sw_val

    # --- Botones ---
    if sq_val == 0 and prev_sq == 1:
        evento = True
        print("BOTON_CUADRADO")
        enviar("CUADRADO")
    prev_sq = sq_val

    if tri_val == 0 and prev_tri == 1:
        evento = True
        print("BOTON_TRIANGULO")
        enviar("TRIANGULO")
    prev_tri = tri_val

    if xbtn_val == 0 and prev_xbtn == 1:
        evento = True
        print("BOTON_X")
        enviar("X")
    prev_xbtn = xbtn_val

    if obtn_val == 0 and prev_obtn == 1:
        evento = True
        print("BOTON_O")
        enviar("O")
    prev_obtn = obtn_val

    # --- Ejes del joystick ---
    if y_val >= 50000 and prev_y < 50000:
        evento = True
        print("Y+")
        enviar("Y+")
    elif y_val <= 15000 and prev_y > 15000:
        evento = True
        print("Y-")
        enviar("Y-")
    prev_y = y_val

    if x_val >= 50000 and prev_x < 50000:
        evento = True
        print("X-")
        enviar("X-")
    elif x_val <= 15000 and prev_x > 15000:
        evento = True
        print("X+")
        enviar("X+")
    prev_x = x_val

    # LED indicador
    if evento:
        led.on()
    else:
        led.off()

    # Recibir comandos del cliente PC
    try:
        data, direccion_cliente = socket_servidor.recvfrom(1024)
        comando = data.decode().strip()
        print("Comando del cliente:", comando)
        enviar("COMANDO_RECIBIDO")
    except OSError:
        pass

    sleep(0.05)
