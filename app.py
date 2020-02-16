import os

from flask import Flask, render_template, flash, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Regexp
from flask_wtf.file import FileAllowed, FileField, FileRequired

app = Flask(__name__)
app.config.from_object('app.config.secure')
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    studentId = db.Column(db.Integer, primary_key=True)
    isolution = db.Column(db.Integer)
    code_color = db.Column(db.Integer)
    submit_time = db.Column(db.DateTime)


class UploadForm(FlaskForm):
    studentId = StringField(label='学号',
                            validators=[DataRequired(), Regexp(r'[0-9]+', message="您输入的学号有误")])
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


@app.route('/')
@app.route('/submitter')
def submitter():
    form = UploadForm()
    return render_template('upload.html', form=form)


@app.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        studentId = form.studentId.data

        filename = '{}.{}'.format(studentId, form.code_photo.data.filename.split('.')[-1])
        form.code_photo.data.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('提交成功', 'success')
        return redirect(url_for('submitter'))
    else:
        errors = ';'.join(i for i in [';'.join(j) for i, j in form.errors.items()])
        flash(errors, 'danger')
        return redirect(url_for('submitter'))


if __name__ == '__main__':
    app.run(port=80)
