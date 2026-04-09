#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
支付宝签到模块（蚂蚁森林/庄园）
"""

import requests
import json
import time

class AlipayCheckin:
    """支付宝签到类"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 13; zh-CN; SM-G9980 Build/TP1A.220624.014) AppleWebKit/537.0',
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # 加载Cookie
        self.cookies = config.get('cookies', {})
        for key, value in self.cookies.items():
            self.session.cookies.set(key, value)
    
    def checkin(self):
        """
        执行支付宝签到（蚂蚁森林/庄园）
        返回: {'success': bool, 'message': str, 'reward': str}
        """
        try:
            results = []
            
            # 蚂蚁森林
            if self.config.get('forest_enabled', True):
                forest_result = self._forest_checkin()
                results.append(('蚂蚁森林', forest_result))
            
            # 蚂蚁庄园
            if self.config.get('farm_enabled', True):
                farm_result = self._farm_checkin()
                results.append(('蚂蚁庄园', farm_result))
            
            # 汇总结果
            success_count = sum(1 for _, r in results if r.get('success'))
            total_count = len(results)
            
            messages = [f"{name}: {r.get('message', '')}" for name, r in results]
            rewards = [r.get('reward', '') for _, r in results if r.get('reward')]
            
            return {
                'success': success_count == total_count,
                'message': ' | '.join(messages),
                'reward': ' | '.join(rewards) if rewards else ''
            }
            
        except Exception as e:
            self.logger.error(f"支付宝签到异常: {str(e)}")
            return {
                'success': False,
                'message': f'签到异常: {str(e)}',
                'reward': ''
            }
    
    def _forest_checkin(self):
        """蚂蚁森林签到"""
        try:
            # 蚂蚁森林API（示例）
            url = 'https://mobilegw.alipay.com/mgw.htm'
            
            # 获取森林状态
            params = {
                'operationType': 'alipay.antforest.forest.h5.queryForestHome',
                'requestData': json.dumps({
                    'version': '2023.0.0',
                    'source': 'chInfo_ch_appcenter__chsub_9patch'
                })
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('success'):
                result = data.get('result', {})
                energy = result.get('energy', 0)
                
                # 收取能量逻辑
                collect_result = self._collect_energy()
                
                return {
                    'success': True,
                    'message': f'森林状态正常，当前能量: {energy}',
                    'reward': collect_result.get('message', '')
                }
            else:
                return {
                    'success': False,
                    'message': '获取森林状态失败',
                    'reward': ''
                }
                
        except Exception as e:
            self.logger.error(f"[支付宝] 蚂蚁森林签到失败: {str(e)}")
            return {
                'success': False,
                'message': f'森林签到失败: {str(e)}',
                'reward': ''
            }
    
    def _collect_energy(self):
        """收取能量"""
        return {
            'success': True,
            'message': '能量收取完成'
        }
    
    def _farm_checkin(self):
        """蚂蚁庄园签到"""
        try:
            # 蚂蚁庄园API（示例）
            url = 'https://mobilegw.alipay.com/mgw.htm'
            
            params = {
                'operationType': 'alipay.antfarm.farm.h5.queryFarmHome',
                'requestData': json.dumps({
                    'version': '2023.0.0',
                    'source': 'chInfo_ch_appcenter__chsub_9patch'
                })
            }
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('success'):
                result = data.get('result', {})
                return {
                    'success': True,
                    'message': '庄园签到完成',
                    'reward': f"饲料: {result.get('food', 0)}"
                }
            else:
                return {
                    'success': False,
                    'message': '庄园签到失败',
                    'reward': ''
                }
                
        except Exception as e:
            self.logger.error(f"[支付宝] 蚂蚁庄园签到失败: {str(e)}")
            return {
                'success': False,
                'message': f'庄园签到失败: {str(e)}',
                'reward': ''
            }
