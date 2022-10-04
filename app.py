from flask import Flask, session,g, request, current_app

import config
from exts import db
from exts import mail

from blueprints import qa_bp
from blueprints import user_bp,teacher_bp
from flask_migrate import Migrate
from utils import jwt_authentication


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)
app.register_blueprint(teacher_bp)

app.before_request(jwt_authentication)


# @app.before_request
# def before_request():
#     user_id = session.get("user_id")
#     if user_id:
#         try:
#             user = UserModel.query.get(user_id)
#             # 给g绑定一个叫做user的变量，他的值是user这个变量
#             setattr(g, "user", user)
#             # g.user = user
#
#         except:
#             g.user = None


# @app.context_processor
# def context_processor():
#     if hasattr(g, "user"):
#         return {"user": g.user}
#     else:
#         return {}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
