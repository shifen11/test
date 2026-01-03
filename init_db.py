"""数据库初始化脚本"""
from backend.database import init_db
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    print("开始初始化数据库...")
    try:
        init_db()
        print("数据库初始化成功！")
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        raise

