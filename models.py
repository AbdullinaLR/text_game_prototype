from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def generate_full_song(song_lines):
    return '\n'.join(song_lines)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    agility = db.Column(db.Integer, nullable=False)
    endurance = db.Column(db.Integer, nullable=False)
    story_index = db.Column(db.Integer, default=0)
    story = db.Column(db.Text, default='')
    enemy_health = db.Column(db.Integer, nullable=True)
    # ДОБАВЛЕНО ДЛЯ ПРОСТО ВЫВОДА
    song_index = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'strength': self.strength,
            'agility': self.agility,
            'endurance': self.endurance,
            'story_index': self.story_index,
            'story': self.story,
            'enemy_health': self.enemy_health,
            # ДОБАВЛЕНО ДЛЯ ПРОСТО ВЫВОДА
            'song_index': self.song_index,


        }
