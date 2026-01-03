"""账户模型"""
from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.model.base import Base

class Account(Base):
    """账户表"""
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True, comment='账户名称')
    account_no = Column(String(20), nullable=False, unique=True, comment='账户号码')
    account_type = Column(String(20), nullable=False, comment='账户类型')
    balance = Column(Float, nullable=False, default=0.0, comment='账户余额')
    credit_limit = Column(Float, nullable=False, default=0.0, comment='信用额度')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关系
    transactions = relationship('Transaction', foreign_keys='Transaction.account_id', back_populates='account', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Account(name='{self.name}', account_no='{self.account_no}', balance={self.balance})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'account_no': self.account_no,
            'account_type': self.account_type,
            'balance': self.balance,
            'credit_limit': self.credit_limit,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

