from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp

from .base import BaseForm


class LoginForm(BaseForm):
    username = StringField(label='用户名（学号）',
                           validators=[DataRequired()])

    password = PasswordField(label='密码',
                             validators=[DataRequired()])

    remember_me = BooleanField(label='记住我')

    submit = SubmitField(label='登录')
