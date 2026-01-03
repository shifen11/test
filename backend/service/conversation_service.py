"""对话服务"""
from typing import List, Dict
from sqlalchemy.orm import Session
from backend.model.conversation import Conversation
from backend.config import Config
import logging

logger = logging.getLogger(__name__)

class ConversationService:
    """对话历史业务逻辑"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_messages(self, session_id: str) -> List[Dict]:
        """获取会话的对话历史"""
        conversations = self.db.query(Conversation)\
            .filter(Conversation.session_id == session_id)\
            .order_by(Conversation.created_at.asc())\
            .limit(Config.MAX_CONVERSATION_HISTORY)\
            .all()
        
        return [conv.to_dict() for conv in conversations]
    
    def add_message(self, session_id: str, role: str, content: str):
        """添加消息到对话历史"""
        conversation = Conversation(
            session_id=session_id,
            role=role,
            content=content
        )
        self.db.add(conversation)
        
        # 清理旧消息，只保留最近的N条
        try:
            count = self.db.query(Conversation)\
                .filter(Conversation.session_id == session_id)\
                .count()
            
            if count > Config.MAX_CONVERSATION_HISTORY:
                # 删除最旧的消息
                oldest = self.db.query(Conversation)\
                    .filter(Conversation.session_id == session_id)\
                    .order_by(Conversation.created_at.asc())\
                    .first()
                if oldest:
                    self.db.delete(oldest)
        
        except Exception as e:
            logger.warning(f"清理旧消息失败: {str(e)}")
        
        self.db.commit()
    
    def clear_conversation(self, session_id: str):
        """清除会话的对话历史"""
        self.db.query(Conversation)\
            .filter(Conversation.session_id == session_id)\
            .delete()
        self.db.commit()

