from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    year = db.Column(db.Integer)
    category = db.Column(db.String(150))
    platform = db.Column(db.String(150))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, title, year, category, platform, price, quantity):
        self.title = title
        self.year = year
        self.category = category
        self.platform = platform
        self.price = price
        self.quantity = quantity
