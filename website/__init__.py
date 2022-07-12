from flask import Flask

def create_app():
    app = Flask(__name__,template_folder='template')
    app.config['SECRET_KEY'] = '123!@_!233S'
    from .view import view
    app.register_blueprint(view)
    return app