from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()
from flask import Flask, render_template, request, redirect, url_for
from models import db, Character
from forms import CharacterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///characters.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_character', methods=['GET', 'POST'])
def create_character():
    form = CharacterForm()
    if form.validate_on_submit():
        character = Character(name=form.name.data, strength=form.strength.data, agility=form.agility.data)
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_character.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

#ffffffffffffffffffffffffffffffffffffffFF

# Писала Ангелина  )))))