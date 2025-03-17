from flask import Flask, render_template
from controllers import routes
from models.database import db
import os

app = Flask(__name__, template_folder='views')


dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(dir, 'models', 'games.sqlite3')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db.init_app(app)

routes.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
        
    app.run(host="localhost", port=5000, debug=True)
