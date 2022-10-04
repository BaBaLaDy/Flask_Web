import wtforms
from wtforms.validators import length,email,EqualTo
from models import EmailCaptchaModel,UserModel

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=30)])

class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3,max=20)])
    student_id = wtforms.StringField(validators=[length(min=3,max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=30)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            print("邮箱验证码错误")
            raise wtforms.ValidationError("邮箱验证码错误")

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            print("邮箱已经存在")
            raise wtforms.ValidationError("邮箱已经存在")

class CreateCourse_Form(wtforms.Form):
    course_id = wtforms.StringField(validators=[length(min=3,max=30)])
    course_name = wtforms.StringField(validators=[length(min=2,max=30)])
    teacher_id = wtforms.StringField(validators=[length(min=3,max=30)])