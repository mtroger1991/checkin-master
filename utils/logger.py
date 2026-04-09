#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志工具模块
"""

import os
import sys
from datetime import datetime
from colorama import init, Fore, Style

# 初始化colorama（跨平台彩色输出）
init(autoreset=True)

class Logger:
    """日志输出类"""
    
    def __init__(self, log_file=None):
        self.log_file = log_file
        self.colors = {
            'info': Fore.CYAN,
            'success': Fore.GREEN,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
            'debug': Fore.MAGENTA
        }
    
    def _log(self, level, message, color=None):
        """输出日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted = f"[{timestamp}] [{level}] {message}"
        
        # 彩色输出
        output_color = color or self.colors.get(level.lower(), '')
        print(f"{output_color}{formatted}{Style.RESET_ALL}")
        
        # 写入文件
        if self.log_file:
            self._write_to_file(formatted)
    
    def _write_to_file(self, message):
        """写入日志文件"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
        except Exception as e:
            print(f"写入日志文件失败: {str(e)}")
    
    def info(self, message):
        """信息日志"""
        self._log('INFO', message, self.colors['info'])
    
    def success(self, message):
        """成功日志"""
        self._log('SUCCESS', message, self.colors['success'])
    
    def warning(self, message):
        """警告日志"""
        self._log('WARNING', message, self.colors['warning'])
    
    def error(self, message):
        """错误日志"""
        self._log('ERROR', message, self.colors['error'])
    
    def debug(self, message):
        """调试日志"""
        self._log('DEBUG', message, self.colors['debug'])
    
    def separator(self, char='-', length=50):
        """分隔线"""
        print(char * length)