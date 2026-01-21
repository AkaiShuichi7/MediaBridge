# -*- coding: utf-8 -*-
"""
@description API 路由控制器
@responsibility 定义前端调用的 RESTful 接口，处理请求参数解析与响应格式化
"""

from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User
from app.core.p115_manager import CookieOnly115Manager

# 定义 API 蓝图，所有路由前缀均为 /api
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/status', methods=['GET'])
def status():
    """
    健康检查接口
    用于前端判断后端服务是否在线
    """
    return jsonify({'status': 'ok', 'message': 'MediaBridge Backend Running'})

@bp.route('/user/cookie', methods=['POST'])
def update_cookie():
    """
    更新用户 Cookie 接口
    
    接收前端提交的 Cookie，调用 p115_manager 进行有效性验证，
    验证通过后存入/更新数据库。
    """
    data = request.json
    cookie = data.get('cookie')
    if not cookie:
        return jsonify({'error': 'Cookie is required'}), 400
    
    # 1. 验证 Cookie 有效性
    try:
        manager = CookieOnly115Manager(cookie)
        user_info = manager.get_user_info()
    except Exception as e:
        # 如果验证失败，直接返回 400 错误
        return jsonify({'error': f'Invalid cookie: {str(e)}'}), 400

    # 2. 存入数据库
    # 查询是否已存在用户记录 (单用户模式)
    user = User.query.first()
    if not user:
        user = User(cookie=cookie)
        db.session.add(user)
    else:
        user.cookie = cookie
    
    db.session.commit()
    
    return jsonify({
        'message': 'Cookie updated successfully',
        'user_info': user_info
    })
