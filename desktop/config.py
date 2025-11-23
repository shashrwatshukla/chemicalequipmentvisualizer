import os

APP_NAME = "Chemical Equipment Visualizer"
APP_VERSION = "1.0.0"
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api')

COLORS = {
    'primary': '#667eea',
    'success': '#11998e',
    'danger': '#f44336',
    'warning': '#ff9800',
    'info': '#2196f3',
    'light': '#f5f7fa',
    'border': '#e0e0e0',
    'background': '#f5f7fa',
}

GRADIENTS = {
    'primary': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2)',
    'success': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #11998e, stop:1 #38ef7d)',
    'danger': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f44336, stop:1 #e91e63)',
    'info': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196f3, stop:1 #00bcd4)',
}