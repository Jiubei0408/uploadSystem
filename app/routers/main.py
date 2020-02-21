import os
import datetime

from flask import Blueprint, flash, current_app, redirect, url_for

from app.forms.upload import UploadForm
from app.models.user import User

from flask import render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    form = UploadForm()
    flash('test', 'success')
    return render_template('upload.html', form=form)


@bp.route('/lists')
def lists():
    content = []
    data = User.search()
    for i in data['data']:
        content.append([i.studentId,
                        i.name,
                        ['0', '是', '否'][i.isolution],
                        ['0', '绿', '黄', '红'][i.code_color],
                        i.submit_time])

    return render_template('list.html',
                           count=data['count'],
                           labels=['学号', '姓名', '是否医学隔离', '健康码状态', '提交时间'],
                           content=content)


@bp.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        studentId = form.studentId.data
        name = form.name.data
        isolution = form.isolution.data
        code_color = form.code_color.data

        user = User.get(studentId=studentId)
        user = User.create(studentId=studentId, times=0) if user is None else user
        times = user.times + 1
        user.modify(isolution=isolution, name=name, code_color=code_color, submit_time=datetime.datetime.now())
        user.modify(times=times)

        filename = '{}-{}.{}'.format(studentId, times, form.code_photo.data.filename.split('.')[-1])
        form.code_photo.data.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))

        flash('提交成功', 'success')
        return redirect(url_for('main.lists'))
    else:
        errors = [j for i, j in form.errors.items()]
        flash('错误:' + errors[0][0], 'danger')
        return redirect(url_for('main.index'))
