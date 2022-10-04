from flask import Blueprint, render_template, g, jsonify
from decorators import login_required
from utils import generate_tokens

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route("/question/public")
@login_required
def public_question():
    # 判断是否登录
    return render_template("public_question.html")


@bp.route("/refesh_jwt")
@login_required
def refesh_jwt():
    """
        刷新token
    """
    user_id = g.user_id
    if user_id and g.is_refresh_token:
        token, refresh_token = generate_tokens(user_id, with_refresh_token=False)
        return jsonify({"code": 200, "message": "success", "token": token, "refresh_token": refresh_token})
    else:
        return jsonify({"code": 403, "message": "Wrong refresh token."})




