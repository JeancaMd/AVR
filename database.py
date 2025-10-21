import pyodbc

class GrupoCajetaDB:
    def __init__(self):
        self.server = "grupocajeta01.database.windows.net"
        self.database = "avatarsvsrooksDB"
        self.db_username = "grupocajeta"
        self.password = "Cajetadecoco01"
        self.driver = "{ODBC Driver 17 for SQL Server}"
        self.connection = None
        self.cursor = None

    def conectar(self):
        try: 
            self.connection = pyodbc.connect(
                f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.db_username};PWD={self.password}'
            )
            self.cursor = self.connection.cursor()
            print('Connection successful')
            return True
    
        except pyodbc.Error as e:
            print('Error de conexion:', e)
            self.connection = None
            self.cursor = None
            return False

    def ingresar_datos(self, username, email, password):
        if not self.cursor:
            print("No hay conexión a la base de datos")
            return False
        
        try:
            self.cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (username, email, password))
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
            return False
        try: 
            self.cursor.execute("SELECT username, password FROM users WHERE username = ? AND password = ?", (username, password))
            result = self.cursor.fetchone()
            if result:
                print("Usuario verificado")
                return True
            else:
                print("Usuario no existente")
                return False
        except pyodbc.Error as e:
            print("Error al verificar:", e)
            return False
        
    # def limpiar_tabla(self):
    #     self.cursor.execute("DELETE from users")
    #     self.connection.commit()

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Conexión cerrada")


# db = GrupoCajetaDB()
# db.conectar()
# db.limpiar_tabla()


