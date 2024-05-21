# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_restful import Api, Resource, reqparse
# import json
# from forms import CharacterForm
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'supersecretkey'
# api = Api(app)
#
# # Временное хранилище персонажей в памяти
# characters = []
#
# def save_characters_to_file():
#     with open('characters.json', 'w') as f:
#         json.dump(characters, f)
#
# def load_characters_from_file():
#     global characters
#     try:
#         with open('characters.json', 'r') as f:
#             characters = json.load(f)
#     except FileNotFoundError:
#         characters = []
#
# load_characters_from_file()
#
# def load_story_from_file(filepath):
#     with open(filepath, 'r', encoding='utf-8') as file:
#         content = file.read()
#     return content.split('\n\n')  # Разделение текста на абзацы по двойным переносам строки
#
# story_paragraphs = load_story_from_file('story.txt')
#
# class CharacterAPI(Resource):
#     def get(self, character_id):
#         character = next((char for char in characters if char['id'] == character_id), None)
#         if character:
#             return character, 200
#         return {"message": "Character not found"}, 404
#
#     def put(self, character_id):
#         parser = reqparse.RequestParser()
#         parser.add_argument('name', type=str)
#         parser.add_argument('strength', type=int)
#         parser.add_argument('agility', type=int)
#         parser.add_argument('endurance', type=int)
#         args = parser.parse_args()
#
#         character = next((char for char in characters if char['id'] == character_id), None)
#         if character:
#             character['name'] = args['name'] if args['name'] else character['name']
#             character['strength'] = args['strength'] if args['strength'] else character['strength']
#             character['agility'] = args['agility'] if args['agility'] else character['agility']
#             character['endurance'] = args['endurance'] if args['endurance'] else character['endurance']
#             save_characters_to_file()
#             return {"message": "Character updated successfully"}, 200
#         return {"message": "Character not found"}, 404
#
#     def delete(self, character_id):
#         global characters
#         character = next((char for char in characters if char['id'] == character_id), None)
#         if character:
#             characters = [char for char in characters if char['id'] != character_id]
#             save_characters_to_file()
#             return {"message": "Character deleted successfully"}, 200
#         return {"message": "Character not found"}, 404
#
# class CharacterListAPI(Resource):
#     def get(self):
#         return characters, 200
#
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('name', type=str, required=True)
#         parser.add_argument('strength', type=int, required=True)
#         parser.add_argument('agility', type=int, required=True)
#         parser.add_argument('endurance', type=int, required=True)
#         args = parser.parse_args()
#
#         new_id = max([char['id'] for char in characters], default=0) + 1
#         character = {
#             'id': new_id,
#             'name': args['name'],
#             'strength': args['strength'],
#             'agility': args['agility'],
#             'endurance': args['endurance'],
#             'story_index': 0,  # Добавляем индекс для отслеживания прогресса по истории
#             'enemy_health': None  # Добавляем поле для здоровья врага
#         }
#         characters.append(character)
#         save_characters_to_file()
#         return {"message": "Character created successfully", "id": character['id']}, 201
#
# api.add_resource(CharacterAPI, '/api/character/<int:character_id>')
# api.add_resource(CharacterListAPI, '/api/characters')
#
# @app.route('/')
# def index():
#     return render_template('index.html', characters=characters)
#
# @app.route('/create_character', methods=['GET', 'POST'])
# def create_character():
#     form = CharacterForm()
#     if form.validate_on_submit():
#         new_id = max([char['id'] for char in characters], default=0) + 1
#         character = {
#             'id': new_id,
#             'name': form.name.data,
#             'strength': form.strength.data,
#             'agility': form.agility.data,
#             'endurance': form.endurance.data,
#             'story_index': 0,  # Добавляем индекс для отслеживания прогресса по истории
#             'enemy_health': None  # Добавляем поле для здоровья врага
#         }
#         characters.append(character)
#         save_characters_to_file()
#         return redirect(url_for('index'))
#     return render_template('create_character.html', form=form)
#
# @app.route('/character/<int:character_id>')
# def character_detail(character_id):
#     character = next((char for char in characters if char['id'] == character_id), None)
#     if not character:
#         return "Character not found", 404
#     return render_template('character_detail.html', character=character)
#
# @app.route('/character/<int:character_id>/delete', methods=['POST'])
# def delete_character(character_id):
#     global characters
#     character = next((char for char in characters if char['id'] == character_id), None)
#     if character:
#         characters = [char for char in characters if char['id'] != character_id]
#         save_characters_to_file()
#         return redirect(url_for('index'))
#     return "Character not found", 404
#
# @app.route('/character/<int:character_id>/start_game', methods=['POST'])
# def start_game(character_id):
#     character = next((char for char in characters if char['id'] == character_id), None)
#     if not character:
#         return "Character not found", 404
#     character['story'] = ''  # Очищаем историю для нового начала
#     character['story_index'] = 0  # Сбрасываем индекс истории
#     character['enemy_health'] = None  # Сбрасываем здоровье врага
#     save_characters_to_file()
#     return redirect(url_for('character_detail', character_id=character_id))
#
# @app.route('/character/<int:character_id>/continue_story', methods=['POST'])
# def continue_story(character_id):
#     character = next((char for char in characters if char['id'] == character_id), None)
#     if not character:
#         return jsonify({"message": "Character not found"}), 404
#
#     if character['story_index'] < len(story_paragraphs):
#         next_paragraph = story_paragraphs[character['story_index']]
#         character['story'] += f'\n\n{next_paragraph}'
#         character['story_index'] += 1
#
#         if "*бой начинается*" in next_paragraph:
#             character['enemy_health'] = 20  # Устанавливаем здоровье врага, например, 50
#         save_characters_to_file()
#         return jsonify({"story": character['story'], "enemy_health": character['enemy_health']}), 200
#     else:
#         return jsonify({"message": "The story has ended"}), 200
#
#
# @app.route('/character/<int:character_id>/attack', methods=['POST'])
# def attack(character_id):
#     character = next((char for char in characters if char['id'] == character_id), None)
#     if not character:
#         return jsonify({"message": "Character not found"}), 404
#
#     if character['enemy_health'] is not None:
#         character['enemy_health'] -= character['strength']
#         if character['enemy_health'] <= 0:
#             character['enemy_health'] = None
#             save_characters_to_file()
#             return jsonify({"message": "Enemy defeated", "story": character['story']}), 200
#         save_characters_to_file()
#         return jsonify({"enemy_health": character['enemy_health']}), 200
#     return jsonify({"message": "No enemy to attack"}), 400
#
#
# if __name__ == "__main__":
#     app.run(debug=True, port=3000, host="127.0.0.1")


from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from forms import CharacterForm
from models import db, Character
from flask_migrate import Migrate

#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'supersecretkey'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///characters.db'
# db.init_app(app)
# api = Api(app)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///characters.db'
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Инициализация базы данных
with app.app_context():
    db.create_all()


# def load_story_from_file(filepath):
#     with open(filepath, 'r', encoding='utf-8') as file:
#         content = file.read()
#     return content.split('\n\n')  # Разделение текста на абзацы по двойным переносам строки
#
#
# story_paragraphs = load_story_from_file('story.txt')

story_paragraphs = []
def load_story_from_file(filepath):
    global story_paragraphs
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    story_paragraphs = content.split('\n\n')

load_story_from_file('story.txt')


# Вспомогательная функция для преобразования объекта Character в словарь
def character_to_dict(character):
    return {
        'id': character.id,
        'name': character.name,
        'strength': character.strength,
        'agility': character.agility,
        'endurance': character.endurance,
        'story_index': character.story_index,
        'enemy_health': character.enemy_health
    }


class CharacterAPI(Resource):
    def get(self, character_id):
        character = Character.query.get(character_id)
        if character:
            return character_to_dict(character), 200
        return {"message": "Character not found"}, 404

    def put(self, character_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('strength', type=int)
        parser.add_argument('agility', type=int)
        parser.add_argument('endurance', type=int)
        args = parser.parse_args()

        character = Character.query.get(character_id)
        if character:
            if args['name']:
                character.name = args['name']
            if args['strength']:
                character.strength = args['strength']
            if args['agility']:
                character.agility = args['agility']
            if args['endurance']:
                character.endurance = args['endurance']
            db.session.commit()
            return {"message": "Character updated successfully"}, 200
        return {"message": "Character not found"}, 404

    def delete(self, character_id):
        character = Character.query.get(character_id)
        if character:
            db.session.delete(character)
            db.session.commit()
            return {"message": "Character deleted successfully"}, 200
        return {"message": "Character not found"}, 404


class CharacterListAPI(Resource):
    def get(self):
        characters = Character.query.all()
        return [character_to_dict(char) for char in characters], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('strength', type=int, required=True)
        parser.add_argument('agility', type=int, required=True)
        parser.add_argument('endurance', type=int, required=True)
        args = parser.parse_args()

        character = Character(
            name=args['name'],
            strength=args['strength'],
            agility=args['agility'],
            endurance=args['endurance']
        )
        db.session.add(character)
        db.session.commit()
        return {"message": "Character created successfully", "id": character.id}, 201


api.add_resource(CharacterAPI, '/api/character/<int:character_id>')
api.add_resource(CharacterListAPI, '/api/characters')


@app.route('/')
def index():
    characters = Character.query.all()
    return render_template('index.html', characters=characters)


@app.route('/create_character', methods=['GET', 'POST'])
def create_character():
    form = CharacterForm()
    if form.validate_on_submit():
        character = Character(
            name=form.name.data,
            strength=form.strength.data,
            agility=form.agility.data,
            endurance=form.endurance.data
        )
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_character.html', form=form)


@app.route('/character/<int:character_id>')
def character_detail(character_id):
    character = Character.query.get(character_id)
    if not character:
        return "Character not found", 404
    return render_template('character_detail.html', character=character)


@app.route('/character/<int:character_id>/delete', methods=['POST'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if character:
        db.session.delete(character)
        db.session.commit()
        return redirect(url_for('index'))
    return "Character not found", 404

@app.route('/character/<int:character_id>/start_game', methods=['POST'])
def start_game(character_id):
    character = Character.query.get(character_id)
    if not character:
        return "Character not found", 404
    character.story = ''  # Очищаем историю для нового начала
    character.story_index = 0  # Сбрасываем индекс истории
    character.enemy_health = None  # Сбрасываем здоровье врага
    db.session.commit()
    return redirect(url_for('character_detail', character_id=character_id))


# @app.route('/character/<int:character_id>/continue_story', methods=['POST'])
# def continue_story(character_id):
#     character = Character.query.get(character_id)
#     if not character:
#         return jsonify({"message": "Character not found"}), 404
#
#     story_paragraphs = load_story_from_file('story.txt')
#     if character.story_index < len(story_paragraphs):
#         next_paragraph = story_paragraphs[character.story_index]
#         character.story_index += 1
#
#         if "*бой начинается*" in next_paragraph:
#             character.enemy_health = 20  # Устанавливаем здоровье врага
#         db.session.commit()
#         return jsonify({"story_index": character.story_index, "enemy_health": character.enemy_health}), 200
#     else:
#         return jsonify({"message": "The story has ended"}), 200
#
#
# @app.route('/character/<int:character_id>/attack', methods=['POST'])
# def attack(character_id):
#     character = Character.query.get(character_id)
#     if not character:
#         return jsonify({"message": "Character not found"}), 404
#
#     if character.enemy_health is not None:
#         character.enemy_health -= character.strength
#         if character.enemy_health <= 0:
#             character.enemy_health = None
#             db.session.commit()
#             return jsonify({"message": "Enemy defeated"}), 200
#         db.session.commit()
#         return jsonify({"enemy_health": character.enemy_health}), 200
#     return jsonify({"message": "No enemy to attack"}), 400

# Определение маршрутов и ресурсов
@app.route('/character/<int:character_id>/continue_story', methods=['POST'])
def continue_story(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"message": "Character not found"}), 404

    if character.story_index < len(story_paragraphs):
        next_paragraph = story_paragraphs[character.story_index]
        character.story += f'\n\n{next_paragraph}'
        character.story_index += 1

        if "*бой начинается*" in next_paragraph:
            character.enemy_health = 20
        db.session.commit()
        return jsonify({"story": character.story, "enemy_health": character.enemy_health}), 200
    else:
        return jsonify({"message": "The story has ended"}), 200

@app.route('/character/<int:character_id>/attack', methods=['POST'])
def attack(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"message": "Character not found"}), 404

    if character.enemy_health is not None:
        character.enemy_health -= character.strength
        if character.enemy_health <= 0:
            character.enemy_health = None
            db.session.commit()
            return jsonify({"message": "Enemy defeated", "story": character.story}), 200
        db.session.commit()
        return jsonify({"enemy_health": character.enemy_health}), 200
    return jsonify({"message": "No enemy to attack"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")
