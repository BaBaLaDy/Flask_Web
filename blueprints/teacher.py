import json

from flask import Blueprint,render_template,request,redirect,url_for,jsonify,session,flash, g
from exts import mail,db
from flask_mail import Message
from models import TeacherModel, CourseModel, AttendenceModel, AttendenceRecordModel, JoinCourseModel, StudentModel
import string
import random
from datetime import datetime,date
from .forms import RegisterForm,LoginForm,CreateCourse_Form,ID_LoginForm,ID_RegisterForm
from werkzeug.security import generate_password_hash,check_password_hash
from utils import generate_tokens
from decorators import login_required

bp = Blueprint("teacher", __name__, url_prefix="/teacher")

"""
处理方法
"""

def query2dict(model_list):
    if isinstance(model_list,list):  #如果传入的参数是一个list类型的，说明是使用的all()的方式查询的
        if isinstance(model_list[0],db.Model):   # 这种方式是获得的整个对象  相当于 select * from table
            lst = []
            for model in model_list:
                dic = {}
                for col in model.__table__.columns:
                    dic[col.name] = getattr(model,col.name)
                lst.append(dic)
            return lst
        else:                           #这种方式获得了数据库中的个别字段  相当于select id,name from table
            lst = []
            for result in model_list:   #当以这种方式返回的时候，result中会有一个keys()的属性
                lst.append([dict(zip(result.keys, r)) for r in result])
            return lst
    else:                   #不是list,说明是用的get() 或者 first()查询的，得到的结果是一个对象
        if isinstance(model_list,db.Model):   # 这种方式是获得的整个对象  相当于 select * from table limit=1
            dic = {}
            for col in model_list.__table__.columns:
                dic[col.name] = getattr(model_list,col.name)
            return dic
        else:    #这种方式获得了数据库中的个别字段  相当于select id,name from table limit = 1
            return dict(zip(model_list.keys(),model_list))




"""老师登录"""
@bp.route('/teacher_login',methods = ["GET","POST"])
def teacher_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = TeacherModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                token, refresh_token = generate_tokens(user.id)
                user_name = user.name
                user_id = user.id
                # session['user_id'] = user.id
                return jsonify({"code": 200, "message": "success", "user_name": user_name, "user_id": user_id, "token": token, "refresh_token": refresh_token})
            else:
                flash("邮箱和密码不匹配！")
                return jsonify({"code": 201, "message": "邮箱和密码不匹配"})
        else:
            flash("邮箱或密码格式错误！")
            return jsonify({"code": 202, "message": "邮箱或密码格式错误"})


@bp.route('/teacher_id_login', methods=["POST"])
def teacher_id_login():
    if request.method == 'POST':
        form = ID_LoginForm(request.form)
        if form.validate():
            id = form.id.data
            password = form.password.data
            user = TeacherModel.query.filter_by(id=id).first()
            if user and check_password_hash(user.password, password):
                token, refresh_token = generate_tokens(user.id)
                user_name = user.name
                user_id = user.id
                #session['user_id'] = user.id
                return jsonify({"code": 200, "message": "success", "user_name": user_name, "user_id": user_id, "token": token, "refresh_token": refresh_token})

            else:
                return jsonify({"code": 201, "message": "邮箱和密码不匹配"})
        else:
            return jsonify({"code": 202, "message": "邮箱或密码格式错误"})


"""老师注册"""
@bp.route('/teacher_register',methods = ["GET","POST"])
def teacher_register():
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
            user = TeacherModel(email=email, name=username, password=hash_password, id=student_id)
            db.session.add(user)
            db.session.commit()
            return jsonify({"code": 200, "message": "regist success"})
        else:
            return jsonify({"code": 400, "message": "regist failed"})


@bp.route('/teacher_id_register', methods=["POST"])
def teacher_id_register():
    if request.method == 'POST':
        form_rg = ID_RegisterForm(request.form)
        if form_rg.validate():
            email = form_rg.email.data
            username = form_rg.username.data
            student_id = form_rg.student_id.data
            password = form_rg.password.data
            # MD5码
            hash_password = generate_password_hash(password)
            user = TeacherModel(email=email, name=username, password=hash_password, id=student_id)
            db.session.add(user)
            db.session.commit()
            return jsonify({"code": 200, "message": "regist success"})
        else:

            return jsonify({"code": 400, "message": "regist failed"})

"""
创建课程
{
    "course_id":543112,
    "course_name":"语文课",
    "teacher_id":2010232
}
"""
@bp.route('/create_course',methods = ["POST"])
@login_required
def creat_course():
    if request.method == 'POST':
        json_data = request.get_json()
        print(json_data)
        if json_data.get('course_id') is None or json_data.get('course_name') is None:
            # code: 400 失败的请求
            return jsonify({"code": 400, "message": "数据输入错误"})
        else:
            course_id = json_data.get('course_id')
            course_name =  json_data.get('course_name')
            teacher_id = g.user_id  # 可从登录信息session中获取
            if CourseModel.query.filter_by(id=course_id).first():
                return jsonify({"code": 401, "message": "该课号已存在"})
            else:
                course = CourseModel(id=course_id, course_name=course_name, teacher_id=teacher_id)
                db.session.add(course)
                db.session.commit()

                # code: 200 成功的、正常的请求
                return jsonify({"code": 200, "message": "success"})


"""
考勤成功记录
{
    "course_id":"123456"
    "student_id":"2000300115"
    "course_time":"二" //代表第二大节打卡
}

"""

@bp.route('/attendance_record',methods = ["POST"])
@login_required
def attendance_record():
    print("enter")
    if request.method == 'POST':
        print("YES")
        json_data = request.get_json()
        print("YES")
        print(json_data)
        if json_data.get('course_id') is None or json_data.get('student_id') is None or json_data.get('course_time') is None:
            # code: 400 失败的请求
            return jsonify({"code": 400, "message": "数据错误"})
        else:
            course_id = json_data.get('course_id')
            course_name = CourseModel.query.filter_by(id=course_id).first().course_name
            student_id = json_data.get('student_id')
            lesson_time = json_data.get('course_time')
            attendance_time = date.today()
            attendance_state = '出勤'

            attendance_data = AttendenceModel(
                                              course_id=course_id,
                                              course_name=course_name,
                                              student_id=student_id,
                                              attendance_time=attendance_time,
                                              lessons_time=lesson_time,
                                              attendance_state=attendance_state,
                                              )
            db.session.add(attendance_data)
            db.session.commit()

            # code: 200 成功的、正常的请求
            return jsonify({"code": 200, "message": "success"})


"""
查询课号是否存在
{
    "course_id":"123456"
}
"""
@bp.route('/check_course_exist',methods = ["POST"])
@login_required
def check_course_exist():
    if request.method == 'POST':
        json_data = request.get_json()
        if json_data == '' or json_data is None:
            # code: 400 失败的请求
            return jsonify({"code": 400, "message": "数据错误"})
        else:
            course_id = json_data.get('course_id')
            if CourseModel.query.filter_by(id=course_id).first():
                # code: 200 成功的、正常的请求
                return jsonify({"code": 200, "message": "课号存在"})
            else:
                # code: 400 失败的请求
                return jsonify({"code": 400, "message": "课号不存在"})

"""
查询考勤
{
    "course_id":123456
}
"""
# @bp.route('/inquire_attendance',methods = ["POST"])
# @login_required
# def inquire_attendance():
#     if request.method == 'POST':
#         json_data = request.get_json()
#         if json_data == '' or json_data is None:
#             # code: 400 失败的请求
#             return jsonify({"code": 400, "message": "数据错误"})
#         else:
#             course_id = json_data.get('course_id')
#             attendance_data = AttendenceModel.query.filter_by(course_id=course_id).all()
#             if attendance_data:
#                 data = query2dict(attendance_data)
#                 print(data)
#                 return jsonify({"code": 200, "message": data})
#             else:
#                 return jsonify({"code": 400, "message": "未查询到相关考勤信息"})

"""
显示创建的所有课号
"""
@bp.route('/inquire_course',methods = ["POST"])
@login_required
def inquire_course():
    if request.method == 'POST':
        teacher_id = g.user_id
        course_data = CourseModel.query.filter_by(teacher_id=teacher_id).all()
        if course_data:
            data = query2dict(course_data)
            print(data)
            return jsonify({"code": 200, "message": data})
        else:
            return jsonify({"code": 400, "message": "未查询到课程信息"})


"""

添加发起考勤记录
{
    "course_id":123456
    "lessons_time":"二"
}
"""
@bp.route('/input_attendenceRecord',methods = ["POST"])
@login_required
def Input_attendenceRecord():
    if request.method == 'POST':
        json_data = request.get_json()
        if json_data == '' or json_data is None:
            # code: 400 失败的请求
            return jsonify({"code": 400, "message": "数据错误"})
        else:
            course_id = json_data.get('course_id')
            course_name = CourseModel.query.filter_by(id=course_id).first().course_name
            attendance_time = date.today()
            print(attendance_time)
            lesson_time = json_data.get('lessons_time')
            record_attendance = AttendenceRecordModel.query.filter_by(course_id=course_id,
                                                                    attendance_time=attendance_time,
                                                                    lessons_time=lesson_time).first()
            print(record_attendance)
            if record_attendance:
                print("记录已存在，直接覆盖")
                db.session.delete(record_attendance)
            input_data = AttendenceRecordModel(
                                            course_id=course_id,
                                            course_name = course_name,
                                            attendance_time=attendance_time,
                                            lessons_time=lesson_time,
            )
            db.session.add(input_data)
            db.session.commit()
            return jsonify({"code": 200, "message": "success"})


"""
查询发考勤记录
{
    "course_id":123456
}
"""
@bp.route('/inquire_attendenceRecord',methods = ["POST"])
@login_required
def inquire_attendenceRecord():
    if request.method == 'POST':
        json_data = request.get_json()
        if json_data == '' or json_data is None:
            # code: 400 失败的请求
            return jsonify({"code": 400, "message": "数据错误"})
        else:
            course_id = json_data.get('course_id')
            record_data = AttendenceRecordModel.query.filter_by(course_id=course_id).all()
            if record_data:
                data = query2dict(record_data)
                print(data)
                return jsonify({"code": 200, "message": data})
            else:
                return jsonify({"code": 400, "message": "未查询到考勤发起信息"})



"""
查询考勤记录
{
    "course_id":123456
    "attendance_time":2022-11-19
    "lessons_time":"二"
}
"""
@bp.route('/inquire_attendance',methods = ["POST"])
@login_required
def inquire_attendance():
    if request.method == 'POST':
        json_data = request.get_json()
        if json_data == '' or json_data is None:
            # code: 400 失败的请求
            return jsonify({"code": 400, "message": "数据错误"})
        else:
            course_id = json_data.get('course_id')
            attendance_time = json_data.get('attendance_time')
            lessons_time = json_data.get('lessons_time')
            attendance_data = AttendenceModel.query.filter_by(course_id=course_id,
                                                              attendance_time=attendance_time,
                                                              lessons_time=lessons_time).all()
            course_data = JoinCourseModel.query.filter_by(course_id=course_id).all()
            a_list = []
            kaoqing_list = []
            if attendance_data:
                a_data = query2dict(attendance_data)
                if course_data:
                    c_data = query2dict(course_data)
                    for i in a_data:
                        json_data = json.dumps(i, ensure_ascii=False)
                        json_data = json.loads(json_data)
                        student_id = json_data['student_id']
                        if student_id not in a_list:
                            a_list.append(student_id)
                            print(a_list)
                            student_name = StudentModel.query.filter_by(id=student_id).first().name
                            chuqing_data = {"attendance_state": "出勤", "student_id": student_id,"student_name":student_name}
                            kaoqing_list.append(chuqing_data)
                    for i in c_data:
                        cjson_data = json.dumps(i, ensure_ascii=False)
                        cjson_data = json.loads(cjson_data)
                        cstudent_id = cjson_data['student_id']
                        if cstudent_id in a_list:
                            pass
                        else:
                            student_name = StudentModel.query.filter_by(id=cstudent_id).first().name
                            queqing_data = {"attendance_state": "缺勤", "student_id": cstudent_id,"student_name":student_name}
                            kaoqing_list.append(queqing_data)

                    return jsonify({"code": 200, "message": kaoqing_list})
            else:
                return jsonify({"code": 400, "message": "查询不到考勤信息"})






















