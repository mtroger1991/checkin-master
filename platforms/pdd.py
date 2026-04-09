#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼多多签到模块
"""

import requests
import json
import hashlib

class PDDCheckin:
    """拼多多签到类"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G9980 Build/TP1A.220624.014) AppleWebKit/537.0',
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'https://mobile.yangkeduo.com/',
        })
        
        # 加载Cookie
        self.cookies = config.get('cookies', {})
        for key, value in self.cookies.items():
            self.session.cookies.set(key, value)
    
    def checkin(self):
        """
        执行拼多多签到
        返回: {'success': bool, 'message': str, 'reward': str}
        """
        try:
            if not self._check_login():
                return {
                    'success': False,
                    'message': 'Cookie已过期，请重新获取',
                    'reward': ''
                }
            
            # 执行签到
            result = self._do_checkin()
            return result
            
        except Exception as e:
            self.logger.error(f"拼多多签到异常: {str(e)}")
            return {
                'success': False,
                'message': f'签到异常: {str(e)}',
                'reward': ''
            }
    
    def _check_login(self):
        """检查登录状态"""
        try:
            url = 'https://api.yangkeduo.com/user'
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            if data.get('is_login'):
                self.logger.info("[拼多多] 登录状态正常")
                return True
            else:
                self.logger.error("[拼多多] 登录已过期")
                return False
                
        except Exception as e:
            self.logger.error(f"[拼多多] 检查登录状态失败: {str(e)}")
            return False
    
    def _do_checkin(self):
        """执行签到逻辑"""
        try:
            # 拼多多果园签到API（示例）
            url = 'https://api.yangkeduo.com/orchard/sign_in'
            
            response = self.session.post(url, json={}, timeout=10)
            data = response.json()
            
            # 解析签到结果
            if data.get('success'):
                result_data = data.get('result', {})
                
                # 检查是否已签到
                if result_data.get('already_signed'):
                    return {
                        'success': True,
                        'message': '今日已签到',
                        'reward': f"水滴: {result_data.get('water', 0)}"
                    }
                
                # 签到成功
                return {
                    'success': True,
                    'message': '签到成功',
                    'reward': f"水滴: {result_data.get('reward_water', 0)}"
                }
            else:
                return {
                    'success': False,
                    'message': data.get('error_msg', '签到失败'),
                    'reward': ''
                }
                
        except Exception as e:
            self.logger.error(f"[拼多多] 签到请求失败: {str(e)}")
            return {
                'success': False,
                'message': f'签到请求失败: {str(e)}',
                'reward': ''
            }
    
    def get_fruit_status(self):
        """获取水果进度"""
        try:
            url = 'https://api.yangkeduo.com/orchard/query_fruit_progress'
            
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            if data.get('success'):
                result = data.get('result', {})
                return {
                    'success': True,
                    'message': f'水果进度: {result.get("progress", 0)}%',
                    'reward': f"水滴: {result.get('water', 0)}"
                }
            else:
                return {
                    'success': False,
                    'message': '获取水果进度失败',
                    'reward': ''
                }
                
        except Exception as e:
            self.logger.error(f"[拼多多] 获取水果进度失败: {str(e)}")
            return {
                'success': False,
                'message': f'获取失败: {str(e)}',
                'reward': ''
            }
