from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Criar a aplicação Flask
app = Flask(__name__)

# Configurar a conexão com o MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/cardapio"
mongo = PyMongo(app)

# Definir a rota principal
@app.route("/")
def index():
    # Obter todos os pratos do banco de dados
    pratos = mongo.db.pratos.find()
    # Renderizar o template index.html com os pratos
    return render_template("index.html", pratos=pratos)

# Definir a rota para adicionar um novo prato
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    # Se o método for POST, obter os dados do formulário
    if request.method == "POST":
        # Criar um dicionário com os dados do prato
        prato = {
            "id": request.form.get("id"),
            "nome": request.form.get("nome"),
            "ingredientes": request.form.get("ingredientes"),
            "preco": request.form.get("preco")
        }
        # Inserir o prato no banco de dados
        mongo.db.pratos.insert_one(prato)
        # Redirecionar para a rota principal
        return redirect(url_for("index"))
    # Se o método for GET, renderizar o template adicionar.html
    return render_template("adicionar.html")

# Definir a rota para atualizar um prato existente
@app.route("/atualizar/<prato_id>", methods=["GET", "POST"])
def atualizar(prato_id):
    # Se o método for POST, obter os dados do formulário
    if request.method == "POST":
        # Criar um dicionário com os novos dados do prato
        novo_prato = {
            "id": request.form.get("id"),
            "nome": request.form.get("nome"),
            "ingredientes": request.form.get("ingredientes"),
            "preco": request.form.get("preco")
        }
        # Atualizar o prato no banco de dados
        mongo.db.pratos.update_one({"_id": ObjectId(prato_id)}, {"$set": novo_prato})
        # Redirecionar para a rota principal
        return redirect(url_for("index"))
    # Se o método for GET, obter o prato do banco de dados
    prato = mongo.db.pratos.find_one({"_id": ObjectId(prato_id)})
    # Renderizar o template atualizar.html com o prato
    return render_template("atualizar.html", prato=prato)

# Definir a rota para deletar um prato
@app.route("/deletar/<prato_id>")
def deletar(prato_id):
    # Deletar o prato do banco de dados
    mongo.db.pratos.delete_one({"_id": ObjectId(prato_id)})
    # Redirecionar para a rota principal
    return redirect(url_for("index"))

# Executar a aplicação
if __name__ == "__main__":
    app.run(debug=True)

