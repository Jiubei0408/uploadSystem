from flask import Blueprint
from flask_login import current_user

from app.forms.login import LoginForm
from app.models.checked_notification import CheckedNotification
from app.models.user import User
from app.models.notifications import Notifications

from flask import render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    res = Notifications.search()
    if current_user.is_anonymous:
        checked_list = {'data': []}
    else:
        checked_list = CheckedNotification.search(user_id=current_user.id)
    return render_template('index.html',
                           user=current_user,
                           checked_list=[i.nf_id for i in checked_list['data']],
                           count=res['count'],
                           data=res['data'])


@bp.route('/lists')
def lists():
    res = User.search()

    return render_template('list.html',
                           count=res['count'],
                           labels=['账号', '姓名', '权限', '时间'],
                           content=[[i.username,
                                     i.nickname,
                                     ['普通用户', '管理员'][i.permission],
                                     i.update_time] for i in res['data']],
                           user=current_user)


@bp.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html',
                           form=form,
                           user=current_user)
