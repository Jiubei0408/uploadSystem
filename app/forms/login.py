from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp

from .base import BaseForm


class LoginForm(BaseForm):
    studentId = StringField(label='用户名（学号）',
                            validators=[DataRequired(), Regexp(r'^[0-9]+$', message="您输入的学号有误")])

    password = PasswordField(label='密码',
                             validators=[DataRequired()])

    remember_me = BooleanField(label='记住我')

    submit = SubmitField(label='登录')
