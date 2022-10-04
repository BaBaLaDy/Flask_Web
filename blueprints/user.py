import json

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash,g
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, StudentModel, CourseModel, JoinCourseModel, TeacherModel, AttendenceModel
import string
import random
from datetime import datetime

from utils import gennerate_tokens
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint("user", __name__, url_prefix="/user")

"""
处理方法
"""


def query2dict(model_list):
    if isinstance(model_list, list):  # 如果传入的参数是一个list类型的，说明是使用的all()的方式查询的
        if isinstance(model_list[0], db.Model):  # 这种方式是获得的整个对象  相当于 select * from table
            lst = []
            for model in model_list:
                dic = {}
                for col in model.__table__.columns:
                    dic[col.name] = getattr(model, col.name)
                lst.append(dic)
            return lst
        else:  # 这种方式获得了数据库中的个别字段  相当于select id,name from table
            lst = []
            for result in model_list:  # 当以这种方式返回的时候，result中会有一个keys()的属性
                lst.append([dict(zip(result.keys, r)) for r in result])
            return lst
    else:  # 不是list,说明是用的get() 或者 first()查询的，得到的结果是一个对象
        if isinstance(model_list, db.Model):  # 这种方式是获得的整个对象  相当于 select * from table limit=1
            dic = {}
            for col in model_list.__table__.columns:
                dic[col.name] = getattr(model_list, col.name)
            return dic
        else:  # 这种方式获得了数据库中的个别字段  相当于select id,name from table limit = 1
            return dict(zip(model_list.keys(), model_list))


"""学生登录"""

@bp.route('/student_login', methods=["GET", "POST"])
def student_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = StudentModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                token, refresh_token = gennerate_tokens(user.id)
                #session['user_id'] = user.id
                return jsonify({"code": 200, "message": "success", "token": token, "refresh_token": refresh_token})

            else:
                flash("邮箱和密码不匹配！")
                return jsonify({"code": 201, "message": "邮箱和密码不匹配"})
        else:
            flash("邮箱或密码格式错误！")
            return jsonify({"code": 202, "message": "邮箱或密码格式错误"})


"""学生注册"""


@bp.route('/student_register', methods=["GET", "POST"])
def student_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form_rg = RegisterForm(request.form)
        if form_rg.validate():
            email = form_rg.email.data
            username = form_rg.username.data
            student_id = form_rg.student_id.data
            password = form_rg.password.data

            # MD5码
            hash_password = generate_password_hash(password)
            user = StudentModel(email=email, name=username, password=hash_password, id=student_id)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:

            return redirect(url_for("user.register"))


"""退出登录"""

@bp.route("/logout")
def logout():
    # 清除session中所有的暑假
    session.clear()
    return redirect(url_for('user.student_login'))


"""获取验证码"""


# memcached/redis/数据库中
@bp.route("/captcha", methods=["POST"])
def get_captcha():
    # GET， POST
    email = request.form.get('email')
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))  # 生成captcha
    if email:
        message = Message(
            subject="【无感考勤平台】验证邮件",
            recipients=[email],
            body=f"【无感考勤平台】您的验证码为：{captcha}, 请勿泄露于他人。",

        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print("captcha:", captcha)

        # code: 200 成功的、正常的请求
        return jsonify({"code": 200, "message": "send captcha success"})


    else:
        # code:400 客户端错误
        return jsonify({"code": 400, "message": "请先传递邮箱"})


"""
学生加入课程
{
    "student_id":2000300115 //从登录信息获取
    "course_id":123456    
}
"""


@bp.route("/join_course", methods=["POST"])
def join_course():
    if request.method == 'POST':
        json_data = request.get_json()
        if json_data == '' or json_data is None:
            # code: 400 失败的请求
            return jsonify({"code": 400, "message": "数据错误"})
        else:
            # 先查询课号是否存在
            course_id = json_data.get('course_id')
            if not CourseModel.query.filter_by(id=course_id).first():
                # code: 400 失败的请求
                return jsonify({"code": 401, "message": "课号不存在"})
            else:
                student_id = json_data.get('student_id')
                course_id = json_data.get('course_id')

                join_data = JoinCourseModel(student_id=student_id, course_id=course_id)
                db.session.add(join_data)
                db.session.commit()
                Course = CourseModel.query.filter_by(id=course_id).first()
                Teacher = TeacherModel.query.filter_by(id=Course.teacher_id).first()

                # code: 200 成功的、正常的请求
                return jsonify({"code": 200, "Teachername": Teacher.name, "Coursename": Course.course_name})


"""
查询考勤情况
{
    "student_id":2000300115
}
"""


@bp.route("/inquire_attendance", methods=["GET"])
def inquire_attendance():
    if request.method == 'GET':
        json_data = request.get_json()
        if json_data == '' or json_data is None:
            # code: 400 失败的请求
            return jsonify({"code": 400, "message": "数据错误"})
        else:
            student_id = json_data.get('student_id')
            attendance_data = AttendenceModel.query.filter_by(student_id=student_id).all()
            count = AttendenceModel.query.filter_by(student_id=student_id).count()
            data = query2dict(attendance_data)
            print(data)
            # print(str(datetime.now()))
            # for i in data:
            #     show = json.dumps(i,ensure_ascii=False)
            #     print(show)

            return jsonify({"code": 200, "message": data})
