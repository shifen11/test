"""对话历史模型"""
from sqlalchemy import Column, String, Text, Integer, DateTime, Index
from datetime import datetime
from backend.model.base import Base

class Conversation(Base):
    """对话历史表"""
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(50), nullable=False, index=True, comment='会话ID')
    role = Column(String(20), nullable=False, comment='角色：user/assistant')
    content = Column(Text, nullable=False, comment='消息内容')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    
    # 创建索引以提高查询性能
    __table_args__ = (
        Index('idx_session_created', 'session_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Conversation(session_id='{self.session_id}', role='{self.role}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'role': self.role,
            'content': self.content
        }

