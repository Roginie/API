
#import para trabalhor com o json
import json
#ferramenta
from flask import Flask, Response, request
#conequicao com banco de dados
from flask_sqlalchemy import SQLAlchemy

#aplicacao do tipo flask
app = Flask('carros')

#havera modificacao no banco de dados
#por padrao em aplicacao em producao isso fica false
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#configuracao de banco de dados 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/bdcarro'

mybd = SQLAlchemy() # Você precisa inicializar o SQLAlchemy

#definir a estrutura da tabela tb_carros
class Carros(mybd.Model):
    id = mybd.Column(mybd.Integer, primary_key=True)  # Corrigi de Interger para Integer
    marca = mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float)
    cor = mybd.Column(mybd.String(100))
    numero_vendas = mybd.Column(mybd.Float)
    ano = mybd.Column(mybd.String(4))
#Convertemos a tabela em json
    def to_json(self):
        # Adicione um bloco de código aqui
        return {
            "id_carro": self.id_carro,
            "marca": self.marca,
            "modelo": self.modelo,
            "valor": self.valor,
            "cor": self.cor,
            "numero_vendas": self.numero_vendas,
            "ano": self.ano
        }
#*****API******
#selecionar tudo (GET)
@app.route("/carros/<id>", methods=["GET"])
def seleciona_carro_id(id):
    carro_objetos = Carros.query.filter_by(id=id).first()

    carro_json = carro_objetos.to_json()

    return gera_response(200, "carros", carro_json)

#Selecionar individual (por ID)
@app.route("/carros", methods=["GET"])
def selecionar_carros():
    carros_objetos = Carros.query.all()

    carro_json = [carro.to_json() for carro in carros_objetos]

    return gera_response(200, "carros", carro_json)

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

#cadastra
@app.route("/carros", methods=["POST"])
def criar_carro():
    body = request.get_json()


    try:
        carro = Carros(id=body["id"], marca=body["marca"], modelo=body[modelo], valor=body[valor], cor=body[cor], numero_vendas=body[numero_vendas],)

        mybd.session.add(carro)
        mybd.session.commit()

        return gera_response(201 "carros", carro.to_json(), "criado com Sucesso!")
    
    except Exception as e:
        print('Erro', e)

        return gera_response(400, "carros", {}, "Erro ao cadastra!!!")
    
    #atualizar
    @app.route("/carro/<id>", methods=["PUT"])
    def atualizar_carro(id):
        carro_objetos = Carros.query.filter_by(id=id).first()
        body = request.get_json()

        try:
            if('marca' in body);
                carro_objetos.marca = body[]