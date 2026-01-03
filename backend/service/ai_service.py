"""AI 服务"""
from openai import OpenAI
from typing import List, Dict
from backend.config import Config
import re
import logging

logger = logging.getLogger(__name__)

class AIService:
    """AI 相关业务逻辑"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=Config.DEEPSEEK_API_KEY,
            base_url=Config.DEEPSEEK_BASE_URL
        )
        self.model = Config.DEEPSEEK_MODEL
    
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """你是一个专业的银行智能助手，名字叫"小银"。你能够帮助用户处理各种银行业务。

你可以执行以下操作（使用CALL:函数名(参数)格式调用）：

1. 查询余额：CALL:get_balance(name="账户名")
2. 查询账户信息：CALL:get_account_info(name="账户名")
3. 转账：CALL:transfer_money(from_name="转出账户", to_name="转入账户", amount=金额)
4. 查询交易记录：CALL:get_transaction_history(name="账户名", limit=数量)
5. 列出所有账户：CALL:list_accounts()

重要规则：
- 当用户询问余额、账户信息、转账、交易记录时，必须使用对应的函数调用
- 转账金额必须是数字，不能包含其他字符
- 如果用户没有明确指定账户名，可以友好地询问
- 对于理财建议、金融知识等咨询类问题，直接回答，不需要调用函数
- 回复要友好、专业、清晰，使用适当的emoji让回复更生动
- 执行操作后，要清晰地展示结果
- 记住之前的对话内容，能够理解上下文和指代关系"""
    
    def chat(self, messages: List[Dict]) -> str:
        """调用 AI 模型进行对话"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI 调用失败: {str(e)}")
            raise
    
    def parse_function_call(self, ai_reply: str) -> tuple:
        """解析AI返回的函数调用指令"""
        if "CALL:" not in ai_reply:
            return None, None
        
        # 匹配函数调用格式
        patterns = {
            "get_balance": r'CALL:get_balance\s*\([^)]*name\s*=\s*["\']([^"\']+)["\']',
            "get_account_info": r'CALL:get_account_info\s*\([^)]*name\s*=\s*["\']([^"\']+)["\']',
            "transfer_money": r'CALL:transfer_money\s*\([^)]*from_name\s*=\s*["\']([^"\']+)["\']\s*,\s*to_name\s*=\s*["\']([^"\']+)["\']\s*,\s*amount\s*=\s*([\d.]+)',
            "get_transaction_history": r'CALL:get_transaction_history\s*\([^)]*name\s*=\s*["\']([^"\']+)["\'](?:\s*,\s*limit\s*=\s*(\d+))?',
            "list_accounts": r'CALL:list_accounts\s*\(\)'
        }
        
        for func_name, pattern in patterns.items():
            match = re.search(pattern, ai_reply, re.IGNORECASE)
            if match:
                if func_name == "transfer_money":
                    return func_name, (match.group(1), match.group(2), float(match.group(3)))
                elif func_name == "get_transaction_history":
                    limit = int(match.group(2)) if match.group(2) else 10
                    return func_name, (match.group(1), limit)
                elif func_name == "list_accounts":
                    return func_name, ()
                else:
                    return func_name, (match.group(1),)
        
        return None, None

