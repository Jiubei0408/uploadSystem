from app.forms.base import BaseForm

from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Regexp
from flask_wtf.file import FileAllowed, FileField, FileRequired


class UploadForm(BaseForm):
    studentId = StringField(label='学号',
                            validators=[DataRequired(), Regexp(r'^[0-9]+$', message="您输入的学号有误")])
    name = StringField(label='姓名',
                       validators=[DataRequired()])
    isolution = SelectField(label='是否被医学隔离',
                            validators=[DataRequired()],
                            choices=[(1, '是'), (2, '否')],
                            coerce=int,
                            default=2)
    code_color = SelectField(label='健康码颜色',
                             validators=[DataRequired()],
                             choices=[(1, '绿色'), (2, '黄色'), (3, '红色')],
                             coerce=int,
                             default=1)
    code_photo = FileField(label='选择文件',
                           validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])],
                           render_kw={
                               'accept': '.jpg, .jpeg, .png, .gif'
                           })
    submit = SubmitField(label='提交')
