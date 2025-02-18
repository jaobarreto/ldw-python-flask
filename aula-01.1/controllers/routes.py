from flask import render_template, request

jogadores = []

def init_app(app):

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():
        game = {'Título': 'League of Legends',
                'Ano': 2009,
                'Categoria': 'Moba'}
        
        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
        return render_template('games.html', game=game, jogadores=jogadores)
