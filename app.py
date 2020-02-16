import os
import datetime

from flask import render_template, flash, url_for, redirect
from flask_bootstrap import Bootstrap
from app.forms.upload import UploadForm

from app import create_app
from app.models.user import User

app = create_app(__name__)

bootstrap = Bootstrap(app)


@app.route('/')
def submitter():
    form = UploadForm()
    return render_template('upload.html', form=form)


@app.route('/list')
def list():
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


@app.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        studentId = form.studentId.data
        name = form.name.data
        isolution = form.isolution.data
        code_color = form.code_color.data

        user = User.get_by_id(studentId)
        user = User.create(studentId=studentId, times=0) if user is None else user
        times = user.times + 1
        user.modify(isolution=isolution, name=name, code_color=code_color, submit_time=datetime.datetime.now())
        user.modify(times=times)

        filename = '{}-{}.{}'.format(studentId, times, form.code_photo.data.filename.split('.')[-1])
        form.code_photo.data.save(os.path.join(app.config['UPLOAD_PATH'], filename))

        flash('提交成功', 'success')
        return redirect(url_for('list'))
    else:
        errors = [j for i, j in form.errors.items()]
        flash('错误:' + errors[0][0], 'danger')
        return redirect(url_for('submitter'))


if __name__ == '__main__':
    app.run(port=80)
