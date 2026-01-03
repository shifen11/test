"""数据库连接和初始化"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
from backend.config import Config
import logging

logger = logging.getLogger(__name__)

# 创建数据库引擎
config = Config()
engine = create_engine(
    config.MYSQL_URI,
    poolclass=NullPool,
    echo=False,
    pool_pre_ping=True,  # 自动重连
    connect_args={
        "charset": "utf8mb4",
        "connect_timeout": 10
    }
)

# 创建会话工厂
SessionLocal = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """初始化数据库表"""
    from backend.model import Base, Account, Transaction, Conversation
    
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
        
        # 初始化默认数据
        init_default_data()
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise

def init_default_data():
    """初始化默认账户数据"""
    from backend.model import Account
    from backend.service.account_service import AccountService
    
    db = SessionLocal()
    try:
        account_service = AccountService(db)
        
        # 检查是否已有数据
        if account_service.get_account_by_name("张三"):
            logger.info("默认数据已存在，跳过初始化")
            return
        
        # 创建默认账户
        default_accounts = [
            {
                "name": "张三",
                "account_no": "6222010012345678",
                "account_type": "储蓄账户",
                "balance": 10000.0,
                "credit_limit": 50000.0
            },
            {
                "name": "李四",
                "account_no": "6222020012345679",
                "account_type": "储蓄账户",
                "balance": 500.0,
                "credit_limit": 20000.0
            },
            {
                "name": "王五",
                "account_no": "6222030012345680",
                "account_type": "理财账户",
                "balance": 50000.0,
                "credit_limit": 100000.0
            }
        ]
        
        for account_data in default_accounts:
            account_service.create_account(**account_data)
        
        logger.info("默认账户数据初始化成功")
    except Exception as e:
        logger.error(f"初始化默认数据失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

