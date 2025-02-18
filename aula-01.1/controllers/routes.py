from flask import render_template, request, redirect, url_for

jogadores = []

gamelist = [{'titulo': 'League of Legends',
             'ano': 2009,
             'categoria': 'Moba'}]


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
                return redirect(url_for('games'))

        return render_template('games.html', game=game, jogadores=jogadores)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gamelist.append(form_data)

        return render_template('cadgames.html', gamelist=gamelist)
