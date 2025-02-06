from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database.config import Session
from models.models import Nutricionista, Paciente, Consulta, Dieta

nutricionista_bp = Blueprint('nutricionista', __name__, url_prefix='/nutricionista', template_folder='templates')

@nutricionista_bp.route('/consulta', methods=['GET', 'POST'])
@login_required
def consulta():
    return render_template('nutricionista/consulta.html')

@nutricionista_bp.route('/dieta', methods=['GET', 'POST'])
@login_required
def dieta():
    return render_template('nutricionista/dieta.html')