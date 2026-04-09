#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通知工具模块
支持：微信推送(Server酱)、邮件通知
"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests

class Notifier:
    """通知类"""
    
    def __init__(self, config):
        self.config = config
        self.enabled = config.get('enabled', False)
        
        # Server酱配置
        self.serverchan_key = config.get('serverchan_key', '')
        
        # 邮件配置
        self.email_config = config.get('email', {})
        
        # Bark配置
        self.bark_key = config.get('bark_key', '')
        
        # PushPlus配置
        self.pushplus_token = config.get('pushplus_token', '')
    
    def send(self, title, message):
        """发送通知"""
        if not self.enabled:
            return
        
        # Server酱
        if self.serverchan_key:
            self._send_serverchan(title, message)
        
        # Bark
        if self.bark_key:
            self._send_bark(title, message)
        
        # PushPlus
        if self.pushplus_token:
            self._send_pushplus(title, message)
        
        # 邮件
        if self.email_config.get('enabled'):
            self._send_email(title, message)
    
    def _send_serverchan(self, title, message):
        """通过Server酱发送微信通知"""
        try:
            url = f'https://sctapi.ftqq.com/{self.serverchan_key}.send'
            data = {
                'title': title,
                'desp': message
            }
            
            response = requests.post(url, data=data, timeout=10)
            result = response.json()
            
            if result.get('code') == 0:
                print("[通知] Server酱发送成功")
            else:
                print(f"[通知] Server酱发送失败: {result.get('message', '')}")
                
        except Exception as e:
            print(f"[通知] Server酱发送异常: {str(e)}")
    
    def _send_bark(self, title, message):
        """通过Bark发送iOS通知"""
        try:
            url = f'https://api.day.app/{self.bark_key}'
            data = {
                'title': title,
                'body': message,
                'sound': 'birdsong'
            }
            
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                print("[通知] Bark发送成功")
            else:
                print(f"[通知] Bark发送失败: {response.status_code}")
                
        except Exception as e:
            print(f"[通知] Bark发送异常: {str(e)}")
    
    def _send_pushplus(self, title, message):
        """通过PushPlus发送微信通知"""
        try:
            url = 'https://www.pushplus.plus/send'
            data = {
                'token': self.pushplus_token,
                'title': title,
                'content': message,
                'template': 'txt'
            }
            
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('code') == 200:
                print("[通知] PushPlus发送成功")
            else:
                print(f"[通知] PushPlus发送失败: {result.get('msg', '')}")
                
        except Exception as e:
            print(f"[通知] PushPlus发送异常: {str(e)}")
    
    def _send_email(self, title, message):
        """通过邮件发送通知"""
        try:
            smtp_server = self.email_config.get('smtp_server', '')
            smtp_port = self.email_config.get('smtp_port', 465)
            sender = self.email_config.get('sender', '')
            password = self.email_config.get('password', '')
            receiver = self.email_config.get('receiver', '')
            
            if not all([smtp_server, sender, password, receiver]):
                print("[通知] 邮件配置不完整")
                return
            
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = title
            
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender, password)
                server.sendmail(sender, receiver, msg.as_string())
            
            print("[通知] 邮件发送成功")
            
        except Exception as e:
            print(f"[通知] 邮件发送异常: {str(e)}")