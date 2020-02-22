from wtforms import StringField
from wtforms.validators import DataRequired

from .base import BaseForm


class AppendNotificationForm(BaseForm):
    content = StringField(label='内容', validators=[DataRequired()])
