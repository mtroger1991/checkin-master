#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美团签到模块
"""

import requests
import json

class MeituanCheckin:
    """美团签到类"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Origin': 'https://i.meituan.com',
            'Referer': 'https://i.meituan.com/',
        })
        
        # 加载token
        self.token = config.get('token', '')
        self.user_id = config.get('user_id', '')
        
        if self.token:
            self.session.headers.update({
                'Cookie': f'token={self.token}'
            })
    
    def checkin(self):
        """
        执行美团签到
        返回: {'success': bool, 'message': str, 'reward': str}
        """
        try:
            if not self.token:
                return {
                    'success': False,
                    'message': '未配置美团token',
                    'reward': ''
                }
            
            # 执行签到
            result = self._do_checkin()
            return result
            
        except Exception as e:
            self.logger.error(f"美团签到异常: {str(e)}")
            return {
                'success': False,
                'message': f'签到异常: {str(e)}',
                'reward': ''
            }
    
    def _do_checkin(self):
        """执行签到逻辑"""
        try:
            # 美团签到API（示例，实际可能需要根据最新接口调整）
            url = 'https://mediacps.meituan.com/gundam/gundamV2'
            
            params = {
                'token': self.token,
                'userId': self.user_id,
                'platform': 'ios',
                'version': '12.0.0'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            # 解析签到结果
            if data.get('code') == 0:
                result_data = data.get('data', {})
                
                # 检查签到状态
                if result_data.get('hasSigned'):
                    return {
                        'success': True,
                        'message': '今日已签到',
                        'reward': result_data.get('signReward', '')
                    }
                
                # 签到成功
                if result_data.get('success'):
                    reward = result_data.get('reward', {})
                    return {
                        'success': True,
                        'message': '签到成功',
                        'reward': f"{reward.get('name', '')} x{reward.get('count', 1)}"
                    }
                
                return {
                    'success': True,
                    'message': '签到完成',
                    'reward': ''
                }
            else:
                return {
                    'success': False,
                    'message': data.get('msg', '签到失败'),
                    'reward': ''
                }
                
        except Exception as e:
            self.logger.error(f"[美团] 签到请求失败: {str(e)}")
            return {
                'success': False,
                'message': f'签到请求失败: {str(e)}',
                'reward': ''
            }
    
    def get_coupons(self):
        """获取当前优惠券列表"""
        try:
            url = 'https://mediacps.meituan.com/gundam/coupons'
            
            params = {
                'token': self.token,
                'userId': self.user_id,
                'status': 'valid'  # 有效优惠券
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('code') == 0:
                coupons = data.get('data', {}).get('coupons', [])
                return {
                    'success': True,
                    'count': len(coupons),
                    'coupons': coupons,
                    'message': f'当前有 {len(coupons)} 张优惠券'
                }
            else:
                return {
                    'success': False,
                    'count': 0,
                    'coupons': [],
                    'message': '获取优惠券失败'
                }
                
        except Exception as e:
            self.logger.error(f"[美团] 获取优惠券失败: {str(e)}")
            return {
                'success': False,
                'count': 0,
                'coupons': [],
                'message': f'获取失败: {str(e)}'
            }
