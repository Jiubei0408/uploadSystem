from app.libs.error import APIException


class Success(APIException):
    code = 200
    msg = 'ok'
    error_code = 0


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999


class ParameterException(APIException):
    code = 400
    msg = '参数错误'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = '找不到该资源'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = '你没有足够的权限'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = '禁止访问'
