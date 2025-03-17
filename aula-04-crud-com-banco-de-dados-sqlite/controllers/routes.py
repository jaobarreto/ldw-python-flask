import urllib.request
from flask import render_template, request, redirect, url_for
from models.database import db, Game
import urllib
import json

jogadores = []
gamelist = [{'Título': 'League of Legends', 'Ano': 2009, 'Categoria': 'MOBA'}]


def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():
        game = gamelist[0]

        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
        return render_template('games.html',
                               game=game,
                               jogadores=jogadores)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            if request.form.get('titulo') and request.form.get('ano') and request.form.get('categoria'):
                gamelist.append({'Título': request.form.get('titulo'), 'Ano': request.form.get(
                    'ano'), 'Categoria': request.form.get('categoria')})

        return render_template('cadgames.html',
                               gamelist=gamelist)

    @app.route('/apigames', methods=['GET', 'POST'])
    # Passando parametros para a rota
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        res = urllib.request.urlopen(url)
        data = res.read()
        gamesjson = json.loads(data)
        # print(gamesjson)

        if id:
            ginfo = []
            for g in gamesjson:
                if g['id'] == id:
                    ginfo = g
                    break
            if ginfo:
                return render_template('gameinfo.html', ginfo=ginfo)
            else:
                return f'Jogo com a ID {id} não encontrado.'

        return render_template('apigames.html', gamesjson=gamesjson)

    @app.route('/estoque', methods=['GET', 'POST'])
    def estoque_view():
        if request.method == 'POST':
            newgame = Game(
                title=request.form.get('title'),
                year=request.form.get('year'),
                category=request.form.get('category'),
                platform=request.form.get('platform'),
                price=request.form.get('price'),
                quantity=request.form.get('quantity')
            )
        db.session.add(newgame)
        db.session.commit()
        return redirect(url_for('estoque_view'))

    gamesestoque = Game.query.all()  # Agora a consulta ocorre dentro do contexto
    return render_template('estoque.html', gamesestoque=gamesestoque)
