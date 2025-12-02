import pyodbc, time, bcrypt

class GrupoCajetaDB:
    def __init__(self):
        self.server = "grupocajeta02.database.windows.net"
        self.database = "avr2"
        self.db_username = "servidor2"
        self.password = "Cajetadecoco02"
        self.driver = "{ODBC Driver 17 for SQL Server}"
        self.connection = None
        self.cursor = None

    def conectar(self, reintentos=3):
        for intento in range(reintentos):
            try:
                self.connection = pyodbc.connect(
                    f'DRIVER={self.driver};'
                    f'SERVER={self.server};'
                    f'DATABASE={self.database};'
                    f'UID={self.db_username};'
                    f'PWD={self.password};'
                    f'Connection Timeout=30;'
                    f'Login Timeout=30',
                )
                self.cursor = self.connection.cursor()
                print('Conectado a base de datos.')
                return True

            except pyodbc.Error as e:
                print(f'Error de conexión (intento {intento + 1}):', e)
                time.sleep(5)

        print('No se pudo conectar a la base de datos')
        self.connection = None
        self.cursor = None
        return False

    def hash_contraseña(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")
    
    def verificar_hashed(self, password, hashed_password):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    def ingresar_datos(self, username, email, password):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return False
        
        try:
            password_hashed = self.hash_contraseña(password)

            self.cursor.execute("INSERT INTO users (username, email, password, theme) VALUES (?,?,?,?)", (username, email, password_hashed, 0))
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print("Error:", e)
            return False
        
    def verificar_usuario(self, username, email, password):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return False
        try:
            self.cursor.execute("SELECT username, email FROM users WHERE username = ? OR email = ?", (username, email))
            result = self.cursor.fetchone()
            if result:
                print("usuario ya existe")
                return False
            else: 
                self.ingresar_datos(username, email, password)
                return True
            
        except pyodbc.Error as e:
            print("Error al verificar usuario:", e)
            return False
        
    def verificar_usuario_existente(self, username, password):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return None
        try: 
            self.cursor.execute(
                "SELECT password, theme FROM users WHERE username = ?",
                (username,)
            )
            result = self.cursor.fetchone()

            if result:
                store_hashed = result[0]
                tema = result[1]

                if self.verificar_hashed(password, store_hashed):
                    print(f"Usuario verificado, tema = {tema}")
                    return tema
                else:
                    print("Contraseña incorrecta")
                    return None
            else:
                print("Usuario no existente")
                return None
        except pyodbc.Error as e:
            print("Error al verificar:", e)
            return None
               
    def actualizar_tema(self, username, tema):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return False
        try:
            self.cursor.execute(
                "UPDATE users SET theme = ? WHERE username = ?",
                (tema, username)
            )
            self.connection.commit()
            print(f"Tema actualizado a {tema} para usuario {username}")
            return True
        except pyodbc.Error as e:
            print("Error al actualizar tema:", e)
            return False
        
    def guardar_puntaje(self, username, puntos, duracion):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return False
        try:
            self.cursor.execute(
                "INSERT INTO scores (username, puntos, duracion, fecha) VALUES (?, ?, ?, GETDATE())",
                (username, puntos, duracion)
            )
            self.connection.commit()
            print(f"Puntaje guardado: {username} - {puntos} puntos")
            return True
        except pyodbc.Error as e:
            print("Error al guardar puntaje:", e)
            return False


    def obtener_mejores_tiempos(self, limite=5):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return []
        try:
            self.cursor.execute(f"""
                SELECT TOP {limite} username, MIN(duracion) AS mejor_tiempo
                FROM scores
                GROUP BY username
                ORDER BY mejor_tiempo ASC
            """)
            resultados = self.cursor.fetchall()
            return [(r[0], r[1]) for r in resultados]
        except pyodbc.Error as e:
            print("Error al obtener mejores tiempos:", e)
            return []


    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Conexión cerrada")

