"""聊天 API"""
from flask import Blueprint, request, jsonify, session
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.service.ai_service import AIService
from backend.service.banking_service import BankingService
from backend.service.conversation_service import ConversationService
import uuid
import logging

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

# 函数映射表
FUNCTION_MAP = {
    "get_balance": "get_balance",
    "get_account_info": "get_account_info",
    "transfer_money": "transfer_money",
    "get_transaction_history": "get_transaction_history",
    "list_accounts": "list_accounts"
}

def get_or_create_session_id():
    """获取或创建会话ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """处理聊天请求"""
    try:
        db: Session = next(get_db())
        user_input = request.json.get("message", "").strip()
        if not user_input:
            return jsonify({"reply": "❌ 请输入您的问题。"}), 400
        
        # 获取或创建会话ID
        session_id = get_or_create_session_id()
        
        # 初始化服务
        ai_service = AIService()
        banking_service = BankingService(db)
        conversation_service = ConversationService(db)
        
        # 获取对话历史
        history_messages = conversation_service.get_messages(session_id)
        
        # 构建完整的消息列表
        api_messages = [{"role": "system", "content": ai_service.get_system_prompt()}]
        if history_messages:
            api_messages.extend(history_messages)
        api_messages.append({"role": "user", "content": user_input})
        
        # 调用AI模型
        ai_reply = ai_service.chat(api_messages)
        
        # 将用户消息添加到对话历史
        conversation_service.add_message(session_id, "user", user_input)
        
        # 检查是否需要执行函数调用
        func_name, func_args = ai_service.parse_function_call(ai_reply)
        
        if func_name and func_name in FUNCTION_MAP:
            try:
                # 执行银行功能
                banking_method = getattr(banking_service, FUNCTION_MAP[func_name])
                if func_args:
                    if isinstance(func_args, tuple):
                        result = banking_method(*func_args)
                    else:
                        result = banking_method(func_args)
                else:
                    result = banking_method()
                
                # 将结果添加到对话历史
                conversation_service.add_message(session_id, "assistant", result)
                return jsonify({"reply": result})
                
            except Exception as e:
                error_msg = f"❌ 执行操作时出错：{str(e)}"
                logger.error(f"执行函数 {func_name} 失败: {str(e)}", exc_info=True)
                conversation_service.add_message(session_id, "assistant", error_msg)
                return jsonify({"reply": error_msg}), 500
        
        # 如果没有函数调用，将AI回复添加到对话历史
        conversation_service.add_message(session_id, "assistant", ai_reply)
        return jsonify({"reply": ai_reply})
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        return jsonify({"reply": f"❌ 系统错误：{str(e)}。请稍后重试。"}), 500

@chat_bp.route('/clear', methods=['POST'])
def clear_conversation():
    """清除对话历史"""
    try:
        db: Session = next(get_db())
        session_id = get_or_create_session_id()
        conversation_service = ConversationService(db)
        conversation_service.clear_conversation(session_id)
        return jsonify({"status": "success", "message": "对话历史已清除"})
    except Exception as e:
        logger.error(f"Clear conversation error: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

