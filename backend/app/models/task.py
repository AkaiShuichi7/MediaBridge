# -*- coding: utf-8 -*-
"""
@description 离线下载任务模型
@responsibility 定义本地任务记录，用于追踪下载状态和重试逻辑
"""

from app import db
from datetime import datetime

class Task(db.Model):
    """
    任务表
    记录从 MediaBridge 发起的所有离线下载任务
    """
    id = db.Column(db.Integer, primary_key=True)
    
    # 原始磁力链接或下载地址
    magnet_link = db.Column(db.Text, nullable=False)
    
    # 任务保存的目标文件夹 ID
    cid = db.Column(db.String(50), nullable=False)
    
    # 任务状态: pending(等待中), downloading(下载中), completed(已完成), failed(失败)
    status = db.Column(db.String(20), default='pending')
    
    # 115 任务的 InfoHash，用于去重和查询
    info_hash = db.Column(db.String(100))
    
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """序列化任务信息"""
        return {
            'id': self.id,
            'magnet_link': self.magnet_link,
            'cid': self.cid,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
