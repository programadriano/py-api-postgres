from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='API de Usuários', description='Uma simples API de usuários')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:102030@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define o modelo de dados com Flask-RESTx
ns = api.namespace('usuarios', description='Operações relacionadas aos usuários')
usuario_model = api.model('Usuario', {
    'id': fields.Integer(readonly=True, description='Identificador único do usuário'),
    'nome': fields.String(required=True, description='Nome do usuário'),
    'email': fields.String(required=True, description='Email do usuário')
})

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

@ns.route('/')
class UsuarioLista(Resource):
    @ns.doc('listar_usuarios')
    @ns.marshal_list_with(usuario_model)
    def get(self):
        '''Listar todos os usuários'''
        return Usuario.query.all()

    @ns.doc('criar_usuario')
    @ns.expect(usuario_model)
    @ns.marshal_with(usuario_model, code=201)
    def post(self):
        '''Criar um novo usuário'''
        dados = request.json
        novo_usuario = Usuario(nome=dados['nome'], email=dados['email'])
        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario, 201

@ns.route('/<int:id>')
@ns.param('id', 'Identificador do usuário')
@ns.response(404, 'Usuário não encontrado')
class UsuarioResource(Resource):
    @ns.doc('pegar_usuario')
    @ns.marshal_with(usuario_model)
    def get(self, id):
        '''Buscar um usuário pelo ID'''
        return Usuario.query.get_or_404(id)

    @ns.doc('atualizar_usuario')
    @ns.expect(usuario_model)
    @ns.marshal_with(usuario_model)
    def put(self, id):
        '''Atualizar um usuário dado o seu ID'''
        usuario = Usuario.query.get_or_404(id)
        dados = request.json
        usuario.nome = dados.get('nome', usuario.nome)
        usuario.email = dados.get('email', usuario.email)
        db.session.commit()
        return usuario

    @ns.doc('deletar_usuario')
    @ns.response(204, 'Usuário deletado')
    def delete(self, id):
        '''Deletar um usuário dado o seu ID'''
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)
