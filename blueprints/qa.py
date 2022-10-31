from flask import Blueprint, render_template, g, jsonify
from decorators import login_required
from utils import generate_tokens

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route('/')
def index():
    return render_template('index.html')









