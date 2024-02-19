from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)

app.config["SECRET_KEY"] = "uma_chave_secreta_muito_segura"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///treino.db"
secrets.token_hex(16)
db = SQLAlchemy(app)

frutas = []
registros = []

class cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    def __init__(self, nome, descricao, ch):
        self.nome = nome
        self.descricao =descricao
        self.ch = ch

@app.route('/', methods=['GET', 'POST'])
def principal():
    if request.method == 'POST':
        if request.form.get('fruta'):
            frutas.append(request.form.get('fruta'))
    return render_template('index.html', frutas=frutas)

@app.route('/sobre', methods=['GET', 'POST'])
def sobre():
    if request.method == 'POST':
        if request.form.get('aluno') and request.form.get('nota'):
            registros.append({'aluno':request.form.get('aluno'),'nota': request.form.get('nota')})
    return render_template('sobre.html', registros=registros)

@app.route('/filmes/<propriedade>')
def filmes(propriedade):
    if propriedade == 'populares':
        url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=39aed0ecbda0ea3404fbb879991ccc3a'
    elif propriedade == 'kdis':
        url ='https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=39aed0ecbda0ea3404fbb879991ccc3a'
    elif propriedade == '2010':
        url= 'https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=39aed0ecbda0ea3404fbb879991ccc3a'
    elif propriedade == 'drama':
        url ='https://api.themoviedb.org/3/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=39aed0ecbda0ea3404fbb879991ccc3a'

    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)
    return render_template("filmes.html", filmes=jsondata['results'])

@app.route('/cursos')
def lista_cursos():
    return render_template('cursos.html', cursos=cursos.query.all())

@app.route('/cria_curso', methods=['GET', 'POST'])
def cria_curso():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    ch = request.form.get('ch')

    if request.method == 'POST':
        if not nome or not descricao or not ch:
            flash('Preencha todos os campos do formulário', 'error')
        else:
            curso = cursos(nome, descricao,ch)
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('lista_cursos'))
    return render_template('novo_curso.html')

if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()