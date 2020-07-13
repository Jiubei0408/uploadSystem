from wtforms import StringField
from wtforms.validators import DataRequired

from .base import BaseForm


class LoginForm(BaseForm):
    username = StringField(validators=[DataRequired(message='用户名不能为空')])
    password = StringField(validators=[DataRequired(message='密码不能为空')])
