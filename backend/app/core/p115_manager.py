# -*- coding: utf-8 -*-
"""
@description 115网盘核心交互管理器
@responsibility 负责与 115 官方 API 进行交互，封装防风控策略（双端轮询、随机延迟、错误熔断）
"""

import time
import random
from p115client import P115Client

class CookieOnly115Manager:
    """
    基于纯 Cookie 的 115 管理器
    不仅实例化客户端，还负责流量控制和端点轮询
    """

    def __init__(self, cookie):
        """
        初始化管理器
        
        :param cookie: 用户的 115 账号 Cookie 字符串
        """
        self.cookie = cookie
        self.client_web = None
        self.client_app = None
        self._init_clients()
        # 调用计数器，用于在 Web 和 App 客户端之间轮询
        self._call_count = 0

    def _init_clients(self):
        """
        初始化 Web 和 iOS 两个不同平台的客户端
        
        策略说明:
        同时持有两种不同 User-Agent 的客户端实例，后续操作时轮询使用，
        模拟用户在网页端和手机端交替操作的行为，降低被判定为机器人的概率。
        """
        try:
            self.client_web = P115Client(self.cookie, app="web")
            self.client_app = P115Client(self.cookie, app="ios")
        except Exception as e:
            # 这里的日志应该接入标准日志系统，暂用 print
            print(f"初始化 115 客户端失败: {e}")
            raise

    def _get_client(self):
        """
        获取当前轮次应该使用的客户端实例
        
        :return: (client_instance, client_mode_name)
        """
        self._call_count += 1
        if self._call_count % 2 == 0:
            return self.client_web, "Web"
        else:
            return self.client_app, "App"

    def get_user_info(self):
        """
        获取用户信息
        
        主要用于验证 Cookie 是否有效。
        Web 端接口通常能返回更详细的会员信息。
        
        :return: 用户信息字典
        """
        try:
            return self.client_web.user_get()
        except Exception as e:
            print(f"获取用户信息失败: {e}")
            raise

    def safe_add_offline_task(self, magnet_links, cid):
        """
        安全添加离线下载任务
        
        包含随机延迟和双端轮询策略。
        
        :param magnet_links: 磁力链接列表或单个字符串
        :param cid: 目标文件夹 ID (Category ID)
        :return: 任务添加结果
        """
        client, mode = self._get_client()
        try:
            # 风控核心策略：添加随机延迟 (2.0 - 5.0秒)
            # 模拟人类复制粘贴链接的耗时
            time.sleep(random.uniform(2.0, 5.0))
            print(f"[{mode}] 正在向 CID {cid} 添加离线任务...")
            
            # p115client 支持直接传入链接列表或单个链接
            result = client.offline_add(magnet_links, cid)
            return result
        except Exception as e:
            # 关键逻辑：捕获验证码错误 (911)
            # 这通常意味着风控等级提升，需要人工干预
            if "code" in str(e) and "911" in str(e):
                print("!!! 检测到验证码挑战 (Code 911) !!!")
                # TODO: 这里应当接入通知系统 (如推送微信/钉钉)
            print(f"[{mode}] 添加任务失败: {e}")
            raise e
            
    def safe_move_files(self, file_ids, target_cid):
        """
        安全移动文件
        
        :param file_ids: 文件 ID 列表
        :param target_cid: 目标文件夹 ID
        :return: 操作结果
        """
        # 移动操作通常在 App 端接口更稳定
        # 但为了安全，这里依然使用轮询获取 client，
        # 如果需要强制使用 App 端，可以直接 self.client_app
        client, mode = self._get_client()
        try:
            # 移动操作的频率限制可以比离线下载稍微宽松一点
            time.sleep(random.uniform(1.5, 3.0))
            return self.client_app.fs_move(file_ids, target_cid)
        except Exception as e:
            print(f"移动文件失败: {e}")
            raise e
