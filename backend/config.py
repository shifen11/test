"""配置文件"""
import os
from typing import Dict

class Config:
    """应用配置"""
    # Flask 配置
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "bank-agent-secret-key-change-in-production")
    
    # DeepSeek API 配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-b7a3837bd39d403aa961e2e95026ee35")
    DEEPSEEK_BASE_URL = "https://api.deepseek.com"
    DEEPSEEK_MODEL = "deepseek-chat"
    
    # MySQL 数据库配置
    MYSQL_HOST = os.getenv("MYSQL_HOST", "sjc1.clusters.zeabur.com")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "23645"))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "2GnCMX97bYN4UmPDup5xqcWjQ81t03S6")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "zeabur")
    
    @property
    def MYSQL_URI(self) -> str:
        """构建 MySQL 连接 URI"""
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
    
    # 对话历史配置
    MAX_CONVERSATION_HISTORY = 100  # 最大对话历史条数

