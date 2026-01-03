"""Flask 应用主文件"""
import os
from flask import Flask, render_template
from backend.config import Config
from backend.database import init_db
from backend.api.chat_api import chat_bp
from backend.api.health_api import health_bp
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_app():
    """应用工厂函数"""
    # 创建 Flask 应用
    app = Flask(__name__, template_folder='frontend')
    app.secret_key = Config.SECRET_KEY

    # 注册蓝图
    app.register_blueprint(chat_bp)
    app.register_blueprint(health_bp)

    @app.route('/')
    def index():
        """首页1"""
        return render_template('index.html')
    
    # 初始化数据库
    try:
        init_db()
        logger.info("数据库初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        # 在生产环境中，如果数据库初始化失败，记录错误但不阻止启动
        # 这样可以先部署应用，再配置数据库
        if os.getenv("FLASK_ENV") == "production":
            logger.warning("生产环境数据库初始化失败，请检查数据库配置")
    
    return app

# 创建应用实例（gunicorn 会使用这个）
app = create_app()

if __name__ == '__main__':
    # 从环境变量获取端口
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
