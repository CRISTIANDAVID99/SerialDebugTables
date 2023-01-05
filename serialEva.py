# Importar las librerías necesarias
import os
import sys
from app import *

# Clase principal de la aplicación
class App:
    def __init__(self):
        # Inicializar variables y configuración de la aplicación
        self.config = {}
        self.data = {}
        
    def run(self):
        # Ejecutar la lógica principal de la aplicación
        serialEva()
        pass

# Función main
def main():
    # Crear una instancia de la clase App
    app = App()
    
    # Ejecutar la aplicación
    app.run()
    
# Llamar a la función main
if __name__ == '__main__':
    main()