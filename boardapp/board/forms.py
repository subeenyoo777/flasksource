from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, PasswordField, EmailField
from wtforms.validators import DataRequired

from wtforms.validators import DataRequired, Email, EqualTo, Length


# 질문등록 관련 form
class QuestionForm(FlaskForm):
    subject = StringField("제목", validators=[DataRequired("제목 필수 입력")])
    content = TextAreaField("내용", validators=[DataRequired("내용 필수 입력")])


# 답변등록 관련 form
class AnswerForm(FlaskForm):
    content = TextAreaField("내용", validators=[DataRequired("내용 필수 입력")])


class UserForm(FlaskForm):
    username = StringField(
        "아이디",
        validators=[
            DataRequired("아이디 필수 입력"),
            Length(min=3, max=20, message="아이디는 3~20자리 사이여야 합니다."),
        ],
    )

    password1 = PasswordField(
        "비밀번호",
        validators=[
            DataRequired("비밀번호 필수 입력"),
            EqualTo("password2", "비밀번호가 일치하지 않습니다"),
        ],
    )
    password2 = PasswordField(
        "비밀번호 확인",
        validators=[DataRequired("비밀번호 필수 입력")],
    )
    email = EmailField(
        "이메일",
        validators=[DataRequired("이메일 필수 입력"), Email("이메일 형식 확인")],
    )


class UserLoginForm(FlaskForm):
    username = StringField(
        "아이디",
        validators=[
            DataRequired("아이디 필수 입력"),
            Length(min=3, max=20, message="아이디 입력."),
        ],
    )

    password = PasswordField(
        "비밀번호",
        validators=[
            DataRequired("비밀번호 입력"),
        ],
    )
