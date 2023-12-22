from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from database import mongo


pratos = Blueprint('pratos', __name__, template_folder='templates')


@pratos.route("/")
def index():
    """ App Index """
    pratos = mongo.db.pratos.find()

    return render_template("index.html", pratos=pratos)


@pratos.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    """ Adiciona um novo prato no menu """

    # Se o método for POST, obter os dados do formulário
    if request.method == "POST":
        prato = {
            "id": request.form.get("id"),
            "nome": request.form.get("nome"),
            "ingredientes": request.form.get("ingredientes"),
            "preco": request.form.get("preco")
        }
        mongo.db.pratos.insert_one(prato)

        return redirect(url_for("pratos.index"))
    
    # Se o método for GET, renderizar o template adicionar.html
    return render_template("adicionar.html")


@pratos.route("/atualizar/<prato_id>", methods=["GET", "POST"])
def atualizar(prato_id):
    """ Atualiza um prato existente no menu """
    # Se o método for POST, obter os dados do formulário
    if request.method == "POST":
        novo_prato = {
            "id": request.form.get("id"),
            "nome": request.form.get("nome"),
            "ingredientes": request.form.get("ingredientes"),
            "preco": request.form.get("preco")
        }
        mongo.db.pratos.update_one({"_id": ObjectId(prato_id)}, {"$set": novo_prato})
        
        return redirect(url_for("pratos.index"))
    # Se o método for GET, obter o prato do banco de dados
    prato = mongo.db.pratos.find_one({"_id": ObjectId(prato_id)})
    
    return render_template("atualizar.html", prato=prato)


@pratos.route("/deletar/<prato_id>")
def deletar(prato_id):
    """ Deleta um prato do menu """
    mongo.db.pratos.delete_one({"_id": ObjectId(prato_id)})
    
    return redirect(url_for("pratos.index"))
