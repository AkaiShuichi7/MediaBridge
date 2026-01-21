# -*- coding: utf-8 -*-
"""
@description 后端启动入口
@responsibility 初始化 Flask 应用并启动 WSGI 服务器
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    # 启动 Flask 开发服务器
    # 注意：端口设置为 5001 以避免与系统常见服务冲突
    app.run(host='0.0.0.0', port=5001, debug=True)
