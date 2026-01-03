import os
import json
from openai import OpenAI

# 1. 配置与初始化
client = OpenAI(
    api_key="sk-b7a3837bd39d403aa961e2e95026ee35", # 建议生产环境使用环境变量
    base_url="https://api.deepseek.com"
)

# 2. 模拟银行数据库 (MVP阶段使用内存字典)
mock_database = {
    "张三": {"balance": 10000.0, "account_no": "622201"},
    "李四": {"balance": 500.0, "account_no": "622202"}
}

# 3. 定义工具函数 (Agent 的“手”)
def get_balance(name):
    """查询指定客户的余额"""
    user = mock_database.get(name)
    if user:
        return f"{name} 的账户余额为: {user['balance']} 元"
    return "未找到该用户信息"

def transfer_money(from_name, to_name, amount):
    """执行转账操作"""
    if from_name not in mock_database or to_name not in mock_database:
        return "转账失败：账户不存在"
    
    if mock_database[from_name]["balance"] < amount:
        return "转账失败：余额不足"
    
    mock_database[from_name]["balance"] -= amount
    mock_database[to_name]["balance"] += amount
    return f"成功从 {from_name} 转账 {amount} 元至 {to_name}。当前余额: {mock_database[from_name]['balance']}"

# 4. Agent 核心逻辑
def run_banking_agent(user_input):
    print(f"\n[用户]: {user_input}")
    
    # 引导模型判断意图并提取参数（简易MVP版：通过Prompt引导模型返回特定格式）
    system_prompt = """
    你是一个银行智能助手。你能帮助用户查询余额和转账。
    
    如果用户想查询余额，请输出格式: CALL:get_balance(name="姓名")
    如果用户想转账，请输出格式: CALL:transfer_money(from_name="谁", to_name="谁", amount=金额)
    如果是普通聊天，直接回复。
    
    当前用户信息：张三、李四。
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        stream=False
    )

    ai_msg = response.choices[0].message.content
    
    # 5. 简单的指令解析与工具调用 (MVP 核心：解析逻辑)
    if "CALL:" in ai_msg:
        # 提取函数调用（实际生产会用 Function Calling 特性，这里为演示 MVP 原理手动解析）
        if "get_balance" in ai_msg:
            name = ai_msg.split('"')[1]
            result = get_balance(name)
        elif "transfer_money" in ai_msg:
            # 简单演示解析：假设模型严格按格式输出
            import re
            params = re.findall(r'"(.*?)"|(\d+)', ai_msg)
            # 提取参数: from_name, to_name, amount
            result = transfer_money(params[0][0], params[1][0], float(params[2][1]))
        
        # 将操作结果反馈给用户
        print(f"[AI 银行助手]: {result}")
    else:
        print(f"[AI 银行助手]: {ai_msg}")

# --- 测试 MVP 应用 ---
if __name__ == "__main__":
    print("--- 欢迎使用智能银行 Agent (MVP版) ---")
    
    # 测试场景 1：查询余额
    run_banking_agent("帮我看看张三还有多少钱？")
    
    # 测试场景 2：转账
    run_banking_agent("给李四转账200块钱，从张三这里扣")
    
    # 测试场景 3：查询转账后的余额
    run_banking_agent("现在张三还有多少钱？")

# 