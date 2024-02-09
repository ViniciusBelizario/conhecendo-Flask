from flask import Flask, render_template, request
import urllib.request, json

app = Flask(__name__)

frutas = []
registros = []

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


if __name__ == "__main__":
    app.run(debug=True)