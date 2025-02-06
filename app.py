from flask import Flask, render_template
from database.config import Session, engine, Base
from flask_login import LoginManager
from controllers.auth_controller import auth_bp, login_manager
from controllers.nutricionista_controller import nutricionista_bp

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'dificil'

login_manager.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(nutricionista_bp)
Base.metadata.create_all(engine)

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/recuperacao", methods=['GET', 'POST'])
def recuperacao():
    return render_template("recuperacao.html")

@app.route("/funcionalidades", methods=['GET', 'POST'])
def funcionalidades():
    return render_template("funcionalidades.html")