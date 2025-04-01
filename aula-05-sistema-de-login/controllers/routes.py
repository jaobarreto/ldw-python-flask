import urllib.request
from flask import render_template, request, redirect, url_for, session, flash
from models.database import db, Game, User
import json
from werkzeug.security import generate_password_hash, check_password_hash

jogadores = []
gamelist = [{'Título': 'League of Legends', 'Ano': 2009, 'Categoria': 'MOBA'}]


def init_app(app):

    @app.before_request
    def check_auth():
        # Rota para login não deve ser verificada para redirecionamento
        routes = ['login', 'cadastro', 'home']

        # Verifica se a rota atual não é 'login' e também se não é um arquivo estático
        if request.endpoint in routes or request.path.startswith('/static/'):
            return

        # Se não houver 'user_id' na sessão, redireciona para login
        if 'user_id' not in session:
            return redirect(url_for('login'))


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

        with app.app_context():
            gamesestoque = Game.query.all()
        return render_template('estoque.html', gamesestoque=gamesestoque)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['email'] = user.email
                nickname = user.email.split('@')
                flash(
                    f'Login bem sucedido! Bem-vindo {nickname[0]}!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Falha Login, Verifique seu nome de usuário e senha', 'danger')

        return render_template('login.html')

    @app.route('/cadastro', methods=['GET', 'POST'])
    def caduser():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            hashed_password = generate_password_hash(password, method='scrypt')
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

        return render_template('caduser.html')

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        session.pop('email', None)
        flash('Logout realizado com sucesso!', 'success')
        return redirect(url_for('home'))
