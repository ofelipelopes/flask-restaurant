# Importar as bibliotecas necessárias
from flask import Flask
from flask_pymongo import PyMongo

# Cria o objeto PyMongo
mongo = PyMongo()

# Configura a conexão com o MongoDB
mongo.init_app(Flask(__name__), uri="mongodb://localhost:27017/cardapio")
