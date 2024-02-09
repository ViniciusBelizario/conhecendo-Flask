import urllib.request, json


url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=39aed0ecbda0ea3404fbb879991ccc3a'

resposta = urllib.request.urlopen(url)

dados = resposta.read()

jsondata = json.loads(dados)

print(jsondata['results'])