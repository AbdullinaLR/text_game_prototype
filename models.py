from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    agility = db.Column(db.Integer, nullable=False)
    endurance = db.Column(db.Integer, nullable=False)
    story = db.Column(db.Text, default='')

    def __repr__(self):
        return f'<Character {self.name}>'
