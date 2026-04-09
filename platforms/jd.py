#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
京东签到模块
"""

import re
import json
import requests
from urllib.parse import urlencode, parse_qs, urlparse

class JDCheckin:
    """京东签到类"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        
        # 加载Cookie
        self.cookies = config.get('cookies', {})
        for key, value in self.cookies.items():
            self.session.cookies.set(key, value)
    
    def checkin(self):
        """
        执行京东签到
        返回: {'success': bool, 'message': str, 'reward': str}
        """
        try:
            # 验证登录状态
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
            self.logger.error(f"京东签到异常: {str(e)}")
            return {
                'success': False,
                'message': f'签到异常: {str(e)}',
                'reward': ''
            }
    
    def _check_login(self):
        """检查登录状态"""
        try:
            url = 'https://plogin.m.jd.com/cgi-bin/ml/islogin'
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            if data.get('islogin') == '1':
                self.logger.info("[京东] 登录状态正常")
                return True
            else:
                self.logger.error("[京东] 登录已过期")
                return False
                
        except Exception as e:
            self.logger.error(f"[京东] 检查登录状态失败: {str(e)}")
            return False
    
    def _do_checkin(self):
        """执行签到逻辑"""
        try:
            # 京东签到API（示例，实际可能需要根据最新接口调整）
            url = 'https://api.m.jd.com/client.action'
            
            # 获取签到页面信息
            params = {
                'functionId': 'signBeanAct',
                'appid': 'ld',
                'client': 'android',
                'clientVersion': '10.0.0'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            # 解析签到结果
            if data.get('code') == '0':
                result_data = data.get('data', {})
                
                # 检查是否已签到
                if result_data.get('status') == '1':
                    return {
                        'success': True,
                        'message': '今日已签到',
                        'reward': result_data.get('dailyAward', {}).get('title', '')
                    }
                
                # 签到成功
                if result_data.get('status') == '2':
                    award = result_data.get('dailyAward', {})
                    return {
                        'success': True,
                        'message': '签到成功',
                        'reward': f"{award.get('title', '')} {award.get('beanAward', {}).get('beanCount', 0)}京豆"
                    }
                
                return {
                    'success': True,
                    'message': result_data.get('statusMessage', '签到完成'),
                    'reward': ''
                }
            else:
                return {
                    'success': False,
                    'message': data.get('msg', '签到失败'),
                    'reward': ''
                }
                
        except Exception as e:
            self.logger.error(f"[京东] 签到请求失败: {str(e)}")
            return {
                'success': False,
                'message': f'签到请求失败: {str(e)}',
                'reward': ''
            }
    
    def get_bean_count(self):
        """获取当前京豆数量"""
        try:
            url = 'https://api.m.jd.com/client.action'
            params = {
                'functionId': 'queryJDUserInfo',
                'appid': 'ld',
                'client': 'android',
                'clientVersion': '10.0.0'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('code') == '0':
                base = data.get('base', {})
                bean_count = base.get('beanCount', 0)
                return {
                    'success': True,
                    'bean_count': bean_count,
                    'message': f'当前京豆: {bean_count}'
                }
            else:
                return {
                    'success': False,
                    'bean_count': 0,
                    'message': '获取京豆数量失败'
                }
                
        except Exception as e:
            self.logger.error(f"[京东] 获取京豆数量失败: {str(e)}")
            return {
                'success': False,
                'bean_count': 0,
                'message': f'获取失败: {str(e)}'
            }
