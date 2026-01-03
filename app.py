import os  # <--- 记得加上这一行，否则会报 NameError
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import re

app = Flask(__name__)

# 配置 DeepSeek
# 建议：在 Zeabur 环境变量里设置 OPENAI_API_KEY，然后用 os.getenv("OPENAI_API_KEY") 读取
client = OpenAI(
    api_key="sk-b7a3837bd39d403aa961e2e95026ee35", 
    base_url="https://api.deepseek.com"
)

# 模拟数据库
mock_db = {
    "张三": {"balance": 10000.0},
    "李四": {"balance": 500.0}
}

def get_balance(name):
    user = mock_db.get(name)
    return f"{name}的当前余额为：{user['balance']}元" if user else "未找到该账户。"

def transfer_money(from_name, to_name, amount):
    if from_name not in mock_db or to_name not in mock_db:
        return "转账失败：账户不存在。"
    try:
        amt = float(amount)
    except:
        return "转账失败：金额格式不正确。"
        
    if mock_db[from_name]["balance"] < amt:
        return "转账失败：余额不足。"
    
    mock_db[from_name]["balance"] -= amt
    mock_db[to_name]["balance"] += amt
    return f"转账成功！已从{from_name}转出{amt}元至{to_name}。"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    
    system_prompt = """你是一个银行助手。你可以执行：
    1. 查询余额: 输出格式 CALL:get_balance(name="姓名")
    2. 转账: 输出格式 CALL:transfer_money(from_name="谁", to_name="谁", amount=金额)
    3. 普通聊天: 直接回复。
    已知账户：张三, 李四。请根据用户需求选择输出。"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ]
        )
        ai_reply = response.choices[0].message.content

        # 解析指令
        if "CALL:" in ai_reply:
            if "get_balance" in ai_reply:
                name = re.search(r'name="(.*?)"', ai_reply).group(1)
                final_res = get_balance(name)
            elif "transfer_money" in ai_reply:
                from_n = re.search(r'from_name="(.*?)"', ai_reply).group(1)
                to_n = re.search(r'to_name="(.*?)"', ai_reply).group(1)
                amt = re.search(r'amount=([\d.]+)', ai_reply).group(1) # 兼容小数点
                final_res = transfer_money(from_n, to_n, amt)
            return jsonify({"reply": final_res})
        
        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"reply": f"错误: {str(e)}"}), 500

if __name__ == '__main__':
    # 从环境变量获取端口，Zeabur 部署必须这么写
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)