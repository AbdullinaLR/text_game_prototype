#
# # НЕ НАДО ВООБЩЕ
# from app import app, db
# from flask_migrate import Migrate
# from flask.cli import with_appcontext
# import click
#
# migrate = Migrate(app, db)
#
# @click.command(name='create_db')
# @with_appcontext
# def create_db():
#     db.create_all()
#
# app.cli.add_command(create_db)
#
# if __name__ == '__main__':
#     app.run()
