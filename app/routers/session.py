from flask import Blueprint, jsonify
from flask_login import current_user, login_required, login_user, logout_user

from app.forms.login import LoginForm
from app.libs.error_code import AuthFailed, Success
from app.models.user import User

bp = Blueprint('session', __name__)


@bp.route('', methods=['GET'])
def get_session():
    user = current_user
    if user.is_anonymous:
        return jsonify({
            'code': 404,
            'data': {
                'username': '',
                'nickname': '',
                'permission': 0
            }
        })
    return jsonify({
        'code': 200,
        'data': {
            'username': user.username,
            'nickname': user.nickname,
            'permission': user.permission
        }
    })


@bp.route('', methods=['POST'])
def login_api():
    form = LoginForm().validate_for_api().data_
    username = form['username']
    password = form['password']
    user = User.get_by_id(username)
    if user is None or user.password != password:
        raise AuthFailed('登录失败，用户名或密码错误')
    login_user(user, remember=False)
    raise Success('登录成功')


@bp.route('', methods=['DELETE'])
@login_required
def logout():
    logout_user()
    raise Success('登出成功')
