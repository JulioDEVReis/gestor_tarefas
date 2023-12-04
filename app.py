from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/tarefas.db'
db = SQLAlchemy(app)

class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True)  #Identificador unico de cada tarefa (não pode ter 2 tarefas com o mesmo id, por isso é primary_key)
    conteúdo = db.Column(db.String(200))  # Conteúdo das tarefas, um texto de máximo 200 caracteres
    feita = db.Column(db.Boolean)  # Booleano que indica se uma tarefa já foi concluida

with app.app_context():
    db.create_all()  # Criaçao das tabelas
    #db.session.commit()  # Execução das tarefas pendentes da base de dados

@app.route('/')
def home():
    todas_as_tarefas = Tarefa.query.all()  # Consultamos e armazenamos todas as tarefas da base de dados
    # Agora, na variavel todas_as_tarefas estão armazenadas todas as tarefas. Vamos entregar essa variavel ao template index.html
    return render_template("index.html", lista_de_tarefas=todas_as_tarefas)   # carrega-se o template index.html

@app.route('/criar-tarefa', methods=['POST'])
def criar():
    #Tarefa é um objeto da classe Tarefa (uma instancia da classe)
    tarefa = Tarefa(conteúdo=request.form['conteúdo_tarefa'], feita=False) # id não é necessário atribui-lo manualmente, porque a primary key gera-se automaticamente
    db.session.add(tarefa)  # Adicionar o objeto da Tarefa à base de dados
    db.session.commit()  #Executar a operação pendente da base de dados
    return redirect(url_for('home'))  # Redirecionamento para 'home'

@app.route('/eliminar-tarefa/<id>')
def eliminar(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).delete() #Pesquisa-se dentro da base de dados, aquele registro cujo id coincida com o proporcionado pelo parametro da rota. Quando encontra-se, elimina-se.
    db.session.commit() #Executar a operação pendente da base de dados
    return redirect(url_for('home'))  # Redirecionamento para 'home'

@app.route('/tarefa-feita/<id>')
def feita(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).first()  # Para obter a tarefa que se procura
    tarefa.feita = not(tarefa.feita)  # Guardar na variável booleana da tarefa, o seu contrário
    db.session.commit()  #Executar a operação pendente da base de dados
    return redirect(url_for('home'))  # Redirecionamento para 'home'

if __name__ == '__main__':
    app.run(debug=True)