#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checkin Master - 多平台自动签到工具
支持：京东、美团、支付宝、拼多多
"""

import os
import sys
import json
import argparse
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from platforms.jd import JDCheckin
from platforms.meituan import MeituanCheckin
from platforms.alipay import AlipayCheckin
from platforms.pdd import PDDCheckin
from utils.logger import Logger
from utils.notifier import Notifier

class CheckinMaster:
    """签到大师主类"""
    
    def __init__(self, config_path='config/config.json'):
        self.config = self._load_config(config_path)
        self.logger = Logger()
        self.notifier = Notifier(self.config.get('notify', {}))
        self.results = []
        
    def _load_config(self, config_path):
        """加载配置文件"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def run_all(self):
        """运行所有平台签到"""
        self.logger.info("=" * 50)
        self.logger.info("开始批量签到任务")
        self.logger.info("=" * 50)
        
        platforms = {
            'jd': JDCheckin,
            'meituan': MeituanCheckin,
            'alipay': AlipayCheckin,
            'pdd': PDDCheckin
        }
        
        for platform_name, platform_class in platforms.items():
            if self.config.get(platform_name, {}).get('enabled', False):
                self._run_platform(platform_name, platform_class)
            else:
                self.logger.info(f"[{platform_name}] 已禁用，跳过")
        
        # 发送通知
        self._send_notification()
        
        self.logger.info("=" * 50)
        self.logger.info("批量签到任务完成")
        self.logger.info("=" * 50)
    
    def _run_platform(self, name, platform_class):
        """运行单个平台签到"""
        self.logger.info(f"\n[{name}] 开始签到...")
        
        try:
            platform_config = self.config.get(name, {})
            checker = platform_class(platform_config, self.logger)
            result = checker.checkin()
            
            self.results.append({
                'platform': name,
                'success': result.get('success', False),
                'message': result.get('message', ''),
                'reward': result.get('reward', '')
            })
            
            if result.get('success'):
                self.logger.success(f"[{name}] 签到成功: {result.get('message', '')}")
                if result.get('reward'):
                    self.logger.info(f"[{name}] 获得奖励: {result.get('reward')}")
            else:
                self.logger.error(f"[{name}] 签到失败: {result.get('message', '')}")
                
        except Exception as e:
            self.logger.error(f"[{name}] 签到异常: {str(e)}")
            self.results.append({
                'platform': name,
                'success': False,
                'message': f'异常: {str(e)}',
                'reward': ''
            })
    
    def _send_notification(self):
        """发送签到结果通知"""
        success_count = sum(1 for r in self.results if r['success'])
        total_count = len(self.results)
        
        title = f"签到完成 - {success_count}/{total_count} 成功"
        
        message = f"签到时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for result in self.results:
            status = "✅" if result['success'] else "❌"
            message += f"{status} {result['platform']}: {result['message']}\n"
            if result['reward']:
                message += f"   奖励: {result['reward']}\n"
        
        self.notifier.send(title, message)

def main():
    parser = argparse.ArgumentParser(description='Checkin Master - 多平台自动签到')
    parser.add_argument('-c', '--config', default='config/config.json', 
                        help='配置文件路径 (默认: config/config.json)')
    parser.add_argument('-p', '--platform', 
                        help='指定平台签到 (jd/meituan/alipay/pdd)')
    
    args = parser.parse_args()
    
    try:
        master = CheckinMaster(args.config)
        
        if args.platform:
            # 单个平台签到
            platform_map = {
                'jd': JDCheckin,
                'meituan': MeituanCheckin,
                'alipay': AlipayCheckin,
                'pdd': PDDCheckin
            }
            
            if args.platform in platform_map:
                master._run_platform(args.platform, platform_map[args.platform])
                master._send_notification()
            else:
                print(f"未知平台: {args.platform}")
                sys.exit(1)
        else:
            # 批量签到
            master.run_all()
            
    except Exception as e:
        print(f"运行失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
