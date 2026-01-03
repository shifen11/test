"""银行业务服务"""
from typing import Optional
from sqlalchemy.orm import Session
from backend.service.account_service import AccountService
import logging

logger = logging.getLogger(__name__)

class BankingService:
    """银行业务逻辑封装"""
    
    def __init__(self, db: Session):
        self.db = db
        self.account_service = AccountService(db)
    
    def get_balance(self, name: str) -> str:
        """查询账户余额"""
        account = self.account_service.get_account_by_name(name)
        if not account:
            return f"❌ 未找到账户名为「{name}」的用户信息。"
        
        return f"✅ 账户信息查询成功\n\n账户名称：{name}\n账户号码：{account.account_no}\n账户类型：{account.account_type}\n当前余额：¥{account.balance:,.2f}元"
    
    def get_account_info(self, name: str) -> str:
        """查询账户详细信息"""
        account = self.account_service.get_account_by_name(name)
        if not account:
            return f"❌ 未找到账户名为「{name}」的用户信息。"
        
        info = f"📋 账户详细信息\n\n"
        info += f"账户名称：{name}\n"
        info += f"账户号码：{account.account_no}\n"
        info += f"账户类型：{account.account_type}\n"
        info += f"当前余额：¥{account.balance:,.2f}元\n"
        info += f"信用额度：¥{account.credit_limit:,.2f}元\n"
        info += f"可用额度：¥{account.credit_limit - account.balance:,.2f}元"
        return info
    
    def transfer_money(self, from_name: str, to_name: str, amount: float) -> str:
        """执行转账"""
        from_account = self.account_service.get_account_by_name(from_name)
        to_account = self.account_service.get_account_by_name(to_name)
        
        if not from_account:
            return f"❌ 转账失败：转出账户「{from_name}」不存在。"
        if not to_account:
            return f"❌ 转账失败：转入账户「{to_name}」不存在。"
        if from_name == to_name:
            return "❌ 转账失败：不能向自己转账。"
        
        try:
            amt = float(amount)
            if amt <= 0:
                return "❌ 转账失败：转账金额必须大于0。"
        except (ValueError, TypeError):
            return "❌ 转账失败：金额格式不正确。"
        
        success, error_msg, txn_id = self.account_service.transfer(
            from_account.id, 
            to_account.id, 
            amt
        )
        
        if not success:
            return f"❌ {error_msg}"
        
        # 重新获取账户信息（余额已更新）
        from_account = self.account_service.get_account_by_id(from_account.id)
        
        result = f"✅ 转账成功！\n\n"
        result += f"交易编号：{txn_id}\n"
        result += f"转出账户：{from_name} ({from_account.account_no})\n"
        result += f"转入账户：{to_name} ({to_account.account_no})\n"
        result += f"转账金额：¥{amt:,.2f}元\n"
        result += f"转出账户余额：¥{from_account.balance:,.2f}元"
        
        return result
    
    def get_transaction_history(self, name: str, limit: int = 10) -> str:
        """查询交易记录"""
        account = self.account_service.get_account_by_name(name)
        if not account:
            return f"❌ 未找到账户名为「{name}」的用户信息。"
        
        transactions = self.account_service.get_transactions(account.id, limit)
        if not transactions:
            return f"📝 {name} 的账户暂无交易记录。"
        
        result = f"📝 {name} 的交易记录（最近{len(transactions)}条）\n\n"
        for txn in transactions:
            txn_dict = txn.to_dict()
            txn_type_emoji = "📤" if txn_dict["type"] == "转出" else "📥"
            result += f"{txn_type_emoji} {txn_dict['timestamp']}\n"
            result += f"   交易编号：{txn_dict['id']}\n"
            result += f"   类型：{txn_dict['type']}\n"
            result += f"   金额：¥{txn_dict['amount']:,.2f}元\n"
            if txn_dict.get("target"):
                result += f"   对方账户：{txn_dict['target']}\n"
            if txn_dict.get("description"):
                result += f"   备注：{txn_dict['description']}\n"
            result += "\n"
        
        return result
    
    def list_accounts(self) -> str:
        """列出所有账户"""
        accounts = self.account_service.get_all_accounts()
        if not accounts:
            return "❌ 系统中暂无账户信息。"
        
        result = "📋 系统账户列表\n\n"
        for account in accounts:
            result += f"账户名称：{account.name}\n"
            result += f"  账户号码：{account.account_no}\n"
            result += f"  账户类型：{account.account_type}\n"
            result += f"  当前余额：¥{account.balance:,.2f}元\n\n"
        
        return result

