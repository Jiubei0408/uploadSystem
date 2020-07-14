from wtforms import StringField
from wtforms.validators import DataRequired

from .base import BaseForm


class AppendNotificationForm(BaseForm):
    title = StringField(validators=[DataRequired()])
    detail = StringField(validators=[DataRequired()])
