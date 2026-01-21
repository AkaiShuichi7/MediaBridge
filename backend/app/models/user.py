# -*- coding: utf-8 -*-
"""
@description 用户数据模型
@responsibility 定义用户表结构，存储 Cookie、User-Agent 及个人设置
"""

from app import db
from datetime import datetime

class User(db.Model):
    """
    用户表
    目前设计为单用户模式，但保留 ID 主键以便未来扩展多用户
    """
    id = db.Column(db.Integer, primary_key=True)
    
    # 用户的 115 Cookie，这是核心凭证
    # 注意：生产环境应考虑加密存储
    cookie = db.Column(db.Text, nullable=False)
    
    # 用户使用的 User-Agent，用于伪装
    ua = db.Column(db.String(255), default='Mozilla/5.0')
    
    # 默认下载目录的 CID (Category ID)
    default_cid = db.Column(db.String(50), default='0')
    
    # 记录最后更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """
        序列化用户信息，用于 API 返回
        注意：出于安全考虑，不返回 cookie 字段
        """
        return {
            'id': self.id,
            'default_cid': self.default_cid,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
