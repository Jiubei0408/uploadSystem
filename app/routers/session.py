from flask import Blueprint, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from app.forms.login import LoginForm
from app.models.user import User

bp = Blueprint('session', __name__)


@bp.route('/login', methods=['POST'])
def login_api():
    form = LoginForm()
    studentId = form.studentId.data
    password = form.password.data
    remember = form.remember_me.data
    user = User.get(studentId=studentId, password=password)
    if user is None:
        flash('登录失败，用户名或密码错误', 'error')
        return redirect(url_for('main.login'))
    flash('登录成功', 'success')
    login_user(user, remember)
    return redirect(url_for('main.index'))


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
