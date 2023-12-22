from flask import Flask
from blueprints.pratos import pratos


app = Flask(__name__)

# Registrar Blueprints
app.register_blueprint(pratos, url_prefix='/pratos')


if __name__ == "__main__":
    app.run(debug=True)
