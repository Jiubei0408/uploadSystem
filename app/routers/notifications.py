from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from app.models.notifications import Notifications
from app.models.checked_notification import CheckedNotification
from app.models.user import User
from app.forms.append_notification import AppendNotificationForm
from app.libs.auth import admin_only
from app.libs.error_code import NotFound, Success, ParameterException

bp = Blueprint('notification', __name__)


@bp.route("/append", methods=['POST'])
@login_required
@admin_only
def append():
    form = AppendNotificationForm()
    content = form.content.data
    Notifications.create(content=content, checked=0, total=User.count(permission=0), username=current_user.username)
    raise Success()


@bp.route("/detail/<int:nf_id>", methods=['POST'])
def detail(nf_id):
    nf = Notifications.get(id=nf_id)
    if nf is None:
        raise NotFound("没有找到该通知")
    result = CheckedNotification.search(nf_id=nf_id, order={'user_id': 'asc'})
    checked = []
    unchecked = []
    for data in result['data']:
        user = User.get(username=data.user_id)
        if user.permission == 0:
            checked.append(user)
    for user in User.search()['data']:
        if user.permission == 1:
            continue
        if user not in checked:
            unchecked.append(user)

    res = {
        'checked': [{'username': user.username,
                     'nickname': user.nickname} for user in checked],
        'unchecked': [{'username': user.username,
                       'nickname': user.nickname} for user in unchecked]
    }
    return jsonify({
        'code': 200,
        'res': res
    })


@bp.route("/check/<int:nf_id>", methods=['POST'])
@login_required
def check(nf_id):
    user = current_user
    nf = Notifications.get(id=nf_id)
    if nf is None:
        raise NotFound()
    if CheckedNotification.get(nf_id=nf.id, user_id=user.id):
        raise ParameterException('你已经确认过了')
    if current_user.permission != 1:
        nf.modify(checked=nf.checked + 1)
    CheckedNotification.create(nf_id=nf.id, user_id=user.id)
    raise Success()
