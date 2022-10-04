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




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run()
