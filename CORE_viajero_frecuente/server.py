from flask_app import app
from flask_app.controllers import usuarios, viajes # Importamos el controlador de usuarios

if __name__ == "__main__":  # Ejecutamos la aplicación

    app.run(debug=True)
