from exts import db
from datetime import datetime


class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)


"""
数据库设计
"""


class StudentModel(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)


class TeacherModel(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)


class CourseModel(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    # teacher = db.relationship('TeacherModel',backref=db.backref('course'))


class AttendenceModel(db.Model):
    __tablename__ = "attendence"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course_name = db.Column(db.String(50), nullable=False)
    attendance_state = db.Column(db.String(50), nullable=False)
    attendance_time = db.Column(db.String(50), default=datetime.now)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    lessons_time = db.Column(db.String(50), nullable=False)
    # student = db.relationship('TeacherModel',backref=db.backref('attendence'))


class JoinCourseModel(db.Model):
    __tablename__ = "joincourse"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
