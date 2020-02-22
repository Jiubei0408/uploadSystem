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
    try:
        Notifications.create(content=content)
    except Exception as e:
        print(e)
    raise Success()


@bp.route("/detail/<int:nf_id>", methods=['POST'])
def detail(nf_id):
    nf = Notifications.get(id=nf_id)
    if nf is None:
        raise NotFound()
    result = CheckedNotification.search(nf_id=nf_id, order={'user_id': 'asc'})
    res = [User.get(username=i.user_id)['nickname'] for i in result['data']]
    return jsonify({
        'code': 200,
        'res': res
    })
    pass


@bp.route("/check/<int:nf_id>", methods=['POST'])
@login_required
def check(nf_id):
    user = current_user
    nf = Notifications.get(id=nf_id)
    if nf is None:
        raise NotFound()
    if CheckedNotification.get(nf_id=nf.id, user_id=user.id):
        raise ParameterException('你已经确认过了')
    nf.modify(checked=nf.checked + 1)
    CheckedNotification.create(nf_id=nf.id, user_id=user.id)
    raise Success()
