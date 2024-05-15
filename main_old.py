from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, reqparse # reqparse получение данных во flask
from flask_restful import Api, Resource
from models import db, Character
from forms import CharacterForm


app = Flask(__name__)
api = Api()
courses = {
    1: {"name": "Python", "videos": 14},
    2: {"name": "C++", "videos": 17}
}
class Main(Resource): ## сможем обрабатывать гет пост и делит запросы
    def get(self, course_id):
        #return {"info":"Some info", "num": 56}## ссоздаем джесон объект
        if course_id ==0:
            return courses
        else:
            return courses[course_id]
    def delite(self, course_id):
        del courses[course_id]
        return courses
    def post(self, course_id): # добавление  по несуществующему id
        parser=reqparse.RequestParser()
        parser.add_argument("name",type=str)
        parser.add_argument("videos", type=int)
        courses[course_id]=parser.parse_args()
        return courses
    def put(self, course_id): # замена содержимого по существующему id
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("videos", type=int)
        courses[course_id] = parser.parse_args()


## обработка url адреа
api.add_resource(Main,"/api/main/<int:course_id>")  ##<>в таких скобках динамический параметр
api.init_app(app)

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


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1") ## любые ошибки и уведы не выводятся в терминале
