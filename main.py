#import para trabalhar com o json
import json
#ferramentas
from flask import Flask, Response, request
#conexão com banco de dados
from flask_sqlalchemy import SQLAlchemy

#aplicação do tipo flask
app = Flask('carros')

#haverá modificação no banco de dados, por padrão em produção isso deve ser False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:senai%40134@127.0.0.1/bdcarro'

# Inicializando o SQLAlchemy com a aplicação Flask
mybd = SQLAlchemy(app)

# Definir a estrutura da tabela tb_carros
class Carros(mybd.Model):
    id = mybd.Column(mybd.Integer, primary_key=True)  # Corrigido para Integer
    marca = mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float)
    cor = mybd.Column(mybd.String(100))
    numero_vendas = mybd.Column(mybd.Float)
    ano = mybd.Column(mybd.String(4))

    # Converter o objeto para JSON
    def to_json(self):
        return {
            "id": self.id,  # Corrigido de id_carro para id
            "marca": self.marca,
            "modelo": self.modelo,
            "valor": self.valor,
            "cor": self.cor,
            "numero_vendas": self.numero_vendas,
            "ano": self.ano
        }

# *****API*****

# Selecionar um carro por ID (GET)
@app.route("/carros/<id>", methods=["GET"])
def seleciona_carro_id(id):
    carro_objeto = Carros.query.filter_by(id=id).first()
    
    if carro_objeto:
        carro_json = carro_objeto.to_json()
        return gera_response(200, "carro", carro_json)
    else:
        return gera_response(404, "carro", {}, "Carro não encontrado")

# Selecionar todos os carros (GET)
@app.route("/carros", methods=["GET"])
def selecionar_carros():
    carros_objetos = Carros.query.all()
    carros_json = [carro.to_json() for carro in carros_objetos]
    return gera_response(200, "carros", carros_json)

# Função para gerar respostas padronizadas
def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if mensagem:
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

# Cadastrar um novo carro (POST)
@app.route("/carros", methods=["POST"])
def criar_carro():
    body = request.get_json()

    try:
        # Criando o novo objeto Carro
        carro = Carros(
            id=body["id"],
            marca=body["marca"],
            modelo=body["modelo"],
            valor=body["valor"],
            cor=body["cor"],
            numero_vendas=body["numero_vendas"],
            ano=body["ano"]
        )

        # Adicionar o carro ao banco de dados
        mybd.session.add(carro)
        mybd.session.commit()

        return gera_response(201, "carro", carro.to_json(), "Criado com Sucesso!")
    
    except Exception as e:
        print('Erro:', e)
        return gera_response(400, "carro", {}, "Erro ao cadastrar o carro")

# Atualizar um carro existente (PUT)
@app.route("/carros/<id>", methods=["PUT"])
def atualizar_carro(id):
    carro_objeto = Carros.query.filter_by(id=id).first()
    body = request.get_json()

    if not carro_objeto:
        return gera_response(404, "carro", {}, "Carro não encontrado")

    try:
        if 'marca' in body:
            carro_objeto.marca = body['marca']
        if 'modelo' in body:
            carro_objeto.modelo = body['modelo']
        if 'valor' in body:
            carro_objeto.valor = body['valor']
        if 'cor' in body:
            carro_objeto.cor = body['cor']
        if 'numero_vendas' in body:
            carro_objeto.numero_vendas = body['numero_vendas']
        if 'ano' in body:
            carro_objeto.ano = body['ano']

        # Salvar as mudanças no banco de dados
        mybd.session.commit()

        return gera_response(200, "carro", carro_objeto.to_json(), "Atualizado com Sucesso!")
    
    except Exception as e:
        print('Erro:', e)
        return gera_response(400, "carro", {}, "Erro ao atualizar o carro")

# Rodar a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)
