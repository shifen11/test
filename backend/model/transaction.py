"""交易记录模型"""
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.model.base import Base

class Transaction(Base):
    """交易记录表"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String(20), nullable=False, unique=True, comment='交易编号')
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False, comment='账户ID')
    transaction_type = Column(String(10), nullable=False, comment='交易类型：转出/转入')
    amount = Column(Float, nullable=False, comment='交易金额')
    target_account_id = Column(Integer, ForeignKey('accounts.id'), nullable=True, comment='对方账户ID')
    description = Column(String(200), nullable=True, comment='交易描述')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    
    # 关系
    account = relationship('Account', foreign_keys=[account_id], back_populates='transactions')
    target_account = relationship('Account', foreign_keys=[target_account_id], viewonly=True)
    
    def __repr__(self):
        return f"<Transaction(transaction_id='{self.transaction_id}', type='{self.transaction_type}', amount={self.amount})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.transaction_id,
            'type': self.transaction_type,
            'amount': self.amount,
            'timestamp': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            'target': self.target_account.name if self.target_account else None,
            'description': self.description
        }

