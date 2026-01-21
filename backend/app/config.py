# -*- coding: utf-8 -*-
"""
@description 后端配置类
@responsibility 管理 Flask 应用的全局配置，包括数据库路径、密钥等
"""

import os

class Config:
    # 基础路径: backend/app/config.py -> backend/app -> backend
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 数据库文件路径: backend/instance/app.db
    # 使用 SQLite 方便部署和迁移
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
    
    # 关闭 SQLAlchemy 的对象修改追踪，减少内存开销
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask Session 密钥，生产环境应通过环境变量设置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
