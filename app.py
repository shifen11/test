import os
from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import re
from datetime import datetime
from typing import Dict, List, Optional
import uuid

app = Flask(__name__)
# 设置secret_key用于session（生产环境建议使用环境变量）
app.secret_key = os.getenv("FLASK_SECRET_KEY", "bank-agent-secret-key-change-in-production")

# 配置 DeepSeek API
# 优先使用环境变量，如果没有则使用默认值（生产环境建议使用环境变量）
api_key = os.getenv("DEEPSEEK_API_KEY", "sk-b7a3837bd39d403aa961e2e95026ee35")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 模拟银行数据库 - 扩展的数据结构
mock_db: Dict[str, Dict] = {
    "张三": {
        "balance": 10000.0,
        "account_no": "6222010012345678",
        "account_type": "储蓄账户",
        "credit_limit": 50000.0,
        "transactions": []
    },
    "李四": {
        "balance": 500.0,
        "account_no": "6222020012345679",
        "account_type": "储蓄账户",
        "credit_limit": 20000.0,
        "transactions": []
    },
    "王五": {
        "balance": 50000.0,
        "account_no": "6222030012345680",
        "account_type": "理财账户",
        "credit_limit": 100000.0,
        "transactions": []
    }
}

# 交易记录ID计数器
transaction_id_counter = 1000

def add_transaction(name: str, transaction_type: str, amount: float, 
                   target_name: Optional[str] = None, description: str = "") -> str:
    """添加交易记录"""
    global transaction_id_counter
    transaction_id_counter += 1
    transaction = {
        "id": f"TXN{transaction_id_counter}",
        "type": transaction_type,
        "amount": amount,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": target_name,
        "description": description
    }
    mock_db[name]["transactions"].append(transaction)
    return transaction["id"]

# ========== 银行功能函数 ==========

def get_balance(name: str) -> str:
    """查询指定客户的账户余额"""
    user = mock_db.get(name)
    if not user:
        return f"❌ 未找到账户名为「{name}」的用户信息。"
    
    balance = user["balance"]
    account_no = user["account_no"]
    return f"✅ 账户信息查询成功\n\n账户名称：{name}\n账户号码：{account_no}\n账户类型：{user['account_type']}\n当前余额：¥{balance:,.2f}元"

def get_account_info(name: str) -> str:
    """查询账户详细信息"""
    user = mock_db.get(name)
    if not user:
        return f"❌ 未找到账户名为「{name}」的用户信息。"
    
    info = f"📋 账户详细信息\n\n"
    info += f"账户名称：{name}\n"
    info += f"账户号码：{user['account_no']}\n"
    info += f"账户类型：{user['account_type']}\n"
    info += f"当前余额：¥{user['balance']:,.2f}元\n"
    info += f"信用额度：¥{user['credit_limit']:,.2f}元\n"
    info += f"可用额度：¥{user['credit_limit'] - user['balance']:,.2f}元"
    return info

def transfer_money(from_name: str, to_name: str, amount: float) -> str:
    """执行转账操作"""
    if from_name not in mock_db:
        return f"❌ 转账失败：转出账户「{from_name}」不存在。"
    if to_name not in mock_db:
        return f"❌ 转账失败：转入账户「{to_name}」不存在。"
    if from_name == to_name:
        return "❌ 转账失败：不能向自己转账。"
    
    try:
        amt = float(amount)
        if amt <= 0:
            return "❌ 转账失败：转账金额必须大于0。"
    except (ValueError, TypeError):
        return "❌ 转账失败：金额格式不正确。"
    
    if mock_db[from_name]["balance"] < amt:
        return f"❌ 转账失败：余额不足。当前余额：¥{mock_db[from_name]['balance']:,.2f}元，转账金额：¥{amt:,.2f}元。"
    
    # 执行转账
    mock_db[from_name]["balance"] -= amt
    mock_db[to_name]["balance"] += amt
    
    # 记录交易
    txn_id_from = add_transaction(from_name, "转出", amt, to_name, f"转账给{to_name}")
    txn_id_to = add_transaction(to_name, "转入", amt, from_name, f"收到{from_name}转账")
    
    result = f"✅ 转账成功！\n\n"
    result += f"交易编号：{txn_id_from}\n"
    result += f"转出账户：{from_name} ({mock_db[from_name]['account_no']})\n"
    result += f"转入账户：{to_name} ({mock_db[to_name]['account_no']})\n"
    result += f"转账金额：¥{amt:,.2f}元\n"
    result += f"转出账户余额：¥{mock_db[from_name]['balance']:,.2f}元"
    
    return result

def get_transaction_history(name: str, limit: int = 10) -> str:
    """查询交易记录"""
    user = mock_db.get(name)
    if not user:
        return f"❌ 未找到账户名为「{name}」的用户信息。"
    
    transactions = user.get("transactions", [])
    if not transactions:
        return f"📝 {name} 的账户暂无交易记录。"
    
    # 按时间倒序，取最近N条
    recent_txns = sorted(transactions, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    result = f"📝 {name} 的交易记录（最近{len(recent_txns)}条）\n\n"
    for txn in recent_txns:
        txn_type_emoji = "📤" if txn["type"] == "转出" else "📥"
        result += f"{txn_type_emoji} {txn['timestamp']}\n"
        result += f"   交易编号：{txn['id']}\n"
        result += f"   类型：{txn['type']}\n"
        result += f"   金额：¥{txn['amount']:,.2f}元\n"
        if txn.get("target"):
            result += f"   对方账户：{txn['target']}\n"
        if txn.get("description"):
            result += f"   备注：{txn['description']}\n"
        result += "\n"
    
    return result

def list_accounts() -> str:
    """列出所有账户"""
    if not mock_db:
        return "❌ 系统中暂无账户信息。"
    
    result = "📋 系统账户列表\n\n"
    for name, info in mock_db.items():
        result += f"账户名称：{name}\n"
        result += f"  账户号码：{info['account_no']}\n"
        result += f"  账户类型：{info['account_type']}\n"
        result += f"  当前余额：¥{info['balance']:,.2f}元\n\n"
    
    return result

# 函数映射表
FUNCTION_MAP = {
    "get_balance": get_balance,
    "get_account_info": get_account_info,
    "transfer_money": transfer_money,
    "get_transaction_history": get_transaction_history,
    "list_accounts": list_accounts
}

def parse_function_call(ai_reply: str) -> Optional[tuple]:
    """解析AI返回的函数调用指令"""
    if "CALL:" not in ai_reply:
        return None
    
    # 匹配函数调用格式：CALL:function_name(param1="value1", param2="value2", param3=123)
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
                return (func_name, match.group(1), match.group(2), float(match.group(3)))
            elif func_name == "get_transaction_history":
                limit = int(match.group(2)) if match.group(2) else 10
                return (func_name, match.group(1), limit)
            elif func_name == "list_accounts":
                return (func_name,)
            else:
                return (func_name, match.group(1))
    
    return None

# 全局存储对话历史（生产环境建议使用Redis等持久化存储）
# 格式：{session_id: [messages]}
conversation_history: Dict[str, List[Dict]] = {}

def get_or_create_session_id():
    """获取或创建会话ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_conversation_messages(session_id: str) -> List[Dict]:
    """获取会话的对话历史"""
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    return conversation_history[session_id]

def add_to_conversation(session_id: str, role: str, content: str):
    """添加消息到对话历史"""
    messages = get_conversation_messages(session_id)
    messages.append({"role": role, "content": content})
    # 限制对话历史长度，避免超出token限制（保留最近50轮对话）
    if len(messages) > 100:  # 50轮对话 = 100条消息（用户+助手）
        messages[:] = messages[-100:]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get("message", "").strip()
        if not user_input:
            return jsonify({"reply": "❌ 请输入您的问题。"}), 400
        
        # 获取或创建会话ID
        session_id = get_or_create_session_id()
        
        # 获取对话历史
        messages = get_conversation_messages(session_id)
        
        # 系统提示词 - 定义智能体的角色和能力
        system_prompt = """你是一个专业的银行智能助手，名字叫"小银"。你能够帮助用户处理各种银行业务。

你可以执行以下操作（使用CALL:函数名(参数)格式调用）：

1. 查询余额：CALL:get_balance(name="账户名")
2. 查询账户信息：CALL:get_account_info(name="账户名")
3. 转账：CALL:transfer_money(from_name="转出账户", to_name="转入账户", amount=金额)
4. 查询交易记录：CALL:get_transaction_history(name="账户名", limit=数量)
5. 列出所有账户：CALL:list_accounts()

当前系统中的账户：张三、李四、王五

重要规则：
- 当用户询问余额、账户信息、转账、交易记录时，必须使用对应的函数调用
- 转账金额必须是数字，不能包含其他字符
- 如果用户没有明确指定账户名，可以友好地询问
- 对于理财建议、金融知识等咨询类问题，直接回答，不需要调用函数
- 回复要友好、专业、清晰，使用适当的emoji让回复更生动
- 执行操作后，要清晰地展示结果
- 记住之前的对话内容，能够理解上下文和指代关系"""
        
        # 构建完整的消息列表（系统提示词 + 对话历史 + 当前用户消息）
        api_messages = [{"role": "system", "content": system_prompt}]
        
        # 添加历史对话（如果存在）
        if messages:
            api_messages.extend(messages)
        
        # 添加当前用户消息
        api_messages.append({"role": "user", "content": user_input})
        
        # 调用AI模型（传递完整的对话历史）
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=api_messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        ai_reply = response.choices[0].message.content
        
        # 将用户消息添加到对话历史
        add_to_conversation(session_id, "user", user_input)
        
        # 检查是否需要执行函数调用
        func_call = parse_function_call(ai_reply)
        
        if func_call:
            func_name = func_call[0]
            if func_name in FUNCTION_MAP:
                try:
                    # 执行函数
                    result = FUNCTION_MAP[func_name](*func_call[1:])
                    # 将函数执行结果作为助手回复添加到历史
                    add_to_conversation(session_id, "assistant", result)
                    return jsonify({"reply": result})
                except Exception as e:
                    error_msg = f"❌ 执行操作时出错：{str(e)}"
                    add_to_conversation(session_id, "assistant", error_msg)
                    return jsonify({"reply": error_msg}), 500
            else:
                error_msg = f"❌ 未知的函数调用：{func_name}"
                add_to_conversation(session_id, "assistant", error_msg)
                return jsonify({"reply": error_msg}), 500
        
        # 如果没有函数调用，将AI回复添加到对话历史
        add_to_conversation(session_id, "assistant", ai_reply)
        
        # 返回AI的回复
        return jsonify({"reply": ai_reply})
    
    except Exception as e:
        app.logger.error(f"Chat error: {str(e)}", exc_info=True)
        return jsonify({"reply": f"❌ 系统错误：{str(e)}。请稍后重试。"}), 500

@app.route('/clear', methods=['POST'])
def clear_conversation():
    """清除当前会话的对话历史"""
    try:
        session_id = get_or_create_session_id()
        if session_id in conversation_history:
            conversation_history[session_id] = []
        return jsonify({"status": "success", "message": "对话历史已清除"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """健康检查接口"""
    return jsonify({"status": "ok", "service": "银行智能体"})

if __name__ == '__main__':
    # 从环境变量获取端口，Zeabur 部署必须这么写
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)