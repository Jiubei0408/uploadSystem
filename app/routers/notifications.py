from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from app.forms.append_notification import AppendNotificationForm
from app.libs.auth import admin_only
from app.libs.error_code import NotFound, ParameterException, Success
from app.models.checked_notification import CheckedNotification
from app.models.notifications import Notifications
from app.models.user import User

bp = Blueprint('notification', __name__)


@bp.route('/append', methods=['POST'])
@login_required
@admin_only
def append():
    form = AppendNotificationForm().validate_for_api().data_
    Notifications.create(confirm_count=0, total=User.count(), creator=current_user.username, **form)
    raise Success()


@bp.route('/summary', methods=['GET'])
def summary():
    raw = Notifications.search(order={'id': 'desc'})
    if current_user.is_anonymous:
        confirmed_list = []
    else:
        confirmed_list = [i.nf_id for i in CheckedNotification.search(user_id=current_user.id)['data']]
    res = [{
        'id': i.id,
        'title': i.title,
        'count': i.confirm_count,
        'confirmed': i.id in confirmed_list,
        'total': i.total,
        'creator': i.creator,
    } for i in raw['data']]
    return jsonify({
        'code': 200,
        'data': res
    })


@bp.route('/detail/<int:nf_id>', methods=['GET'])
def detail(nf_id):
    nf = Notifications.get_by_id(nf_id)
    if nf is None:
        raise NotFound("没有找到该通知")
    return jsonify({
        'code': 200,
        'data': nf.detail
    })


@bp.route('/confirm_detail/<int:nf_id>', methods=['GET'])
@login_required
@admin_only
def confirm_detail(nf_id):
    nf = Notifications.get(id=nf_id)
    if nf is None:
        raise NotFound("没有找到该通知")
    result = CheckedNotification.search(nf_id=nf_id, order={'user_id': 'asc'})
    checked = []
    unchecked = []
    for data in result['data']:
        user = User.get(username=data.user_id)
        checked.append(user)
    for user in User.search()['data']:
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


@bp.route('/confirm/<int:nf_id>', methods=['POST'])
@login_required
def confirm(nf_id):
    user = current_user
    nf = Notifications.get_by_id(nf_id)
    if nf is None:
        raise NotFound('找不到这个通知')
    if CheckedNotification.get(nf_id=nf.id, user_id=user.id):
        raise ParameterException('你已经确认过了')
    nf.modify(confirm_count=nf.confirm_count + 1)
    CheckedNotification.create(nf_id=nf.id, user_id=user.id)
    raise Success()


@bp.route('/<int:nf_id>', methods=['DELETE'])
@login_required
@admin_only
def delete(nf_id):
    nf = Notifications.get_by_id(nf_id)
    if nf is None:
        raise NotFound('找不到这个通知')
    nf.delete()
    raise Success('已删除')


@bp.route('/test', methods=['POST'])
@login_required
@admin_only
def generate_test():
    checks = CheckedNotification.search()['data']
    for check in checks:
        check.delete()
    nfs = Notifications.search()['data']
    for nf in nfs:
        nf.delete()

    for i in range(1, 11):
        data = {
            'confirm_count': 0,
            'total': User.count(),
            'creator': current_user.username,
            'title': 'test' + str(i),
            'detail': 'detail ' * i
        }
        Notifications.create(**data)
    CheckedNotification.create(nf_id=3, user_id=2)
    nf = Notifications.get_by_id(3)
    nf.modify(confirm_count=nf.confirm_count + 1)
    raise Success('generated')
