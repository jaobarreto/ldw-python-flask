from flask import Flask, render_template
from controllers import routes
from models.database import db
import os

app = Flask(__name__, template_folder='views')
routes.init_app(app)

dir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(dir, 'models', 'games.sqlite3')}"

if __name__ == '__main__':
    db.init_app(app)  # Inicializa o banco com o app
    with app.app_context():  # Cria um contexto da aplicação
        db.create_all()  # Agora pode criar as tabelas
    
    app.run(host="localhost", port=5000, debug=True)
