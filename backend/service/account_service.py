"""账户服务"""
from typing import Optional, List
from sqlalchemy.orm import Session
from backend.model.account import Account
from backend.model.transaction import Transaction
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AccountService:
    """账户业务逻辑"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_account_by_name(self, name: str) -> Optional[Account]:
        """根据名称获取账户"""
        return self.db.query(Account).filter(Account.name == name).first()
    
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """根据ID获取账户"""
        return self.db.query(Account).filter(Account.id == account_id).first()
    
    def get_all_accounts(self) -> List[Account]:
        """获取所有账户"""
        return self.db.query(Account).all()
    
    def create_account(self, name: str, account_no: str, account_type: str, 
                      balance: float = 0.0, credit_limit: float = 0.0) -> Account:
        """创建账户"""
        account = Account(
            name=name,
            account_no=account_no,
            account_type=account_type,
            balance=balance,
            credit_limit=credit_limit
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def update_balance(self, account_id: int, amount: float) -> bool:
        """更新账户余额"""
        account = self.get_account_by_id(account_id)
        if not account:
            return False
        account.balance += amount
        account.updated_at = datetime.now()
        self.db.commit()
        return True
    
    def transfer(self, from_account_id: int, to_account_id: int, amount: float):
        """
        执行转账
        返回: (是否成功, 错误信息, 交易编号)
        """
        from_account = self.get_account_by_id(from_account_id)
        to_account = self.get_account_by_id(to_account_id)
        
        if not from_account:
            return False, f"转出账户不存在", None
        if not to_account:
            return False, f"转入账户不存在", None
        if from_account_id == to_account_id:
            return False, "不能向自己转账", None
        if amount <= 0:
            return False, "转账金额必须大于0", None
        if from_account.balance < amount:
            return False, f"余额不足。当前余额：¥{from_account.balance:,.2f}元，转账金额：¥{amount:,.2f}元", None
        
        try:
            # 更新余额
            from_account.balance -= amount
            to_account.balance += amount
            from_account.updated_at = datetime.now()
            to_account.updated_at = datetime.now()
            
            # 生成交易编号
            transaction_id = self._generate_transaction_id()
            
            # 创建交易记录（转出）
            from_transaction = Transaction(
                transaction_id=f"{transaction_id}_FROM",
                account_id=from_account_id,
                transaction_type="转出",
                amount=amount,
                target_account_id=to_account_id,
                description=f"转账给{to_account.name}"
            )
            
            # 创建交易记录（转入）
            to_transaction = Transaction(
                transaction_id=f"{transaction_id}_TO",
                account_id=to_account_id,
                transaction_type="转入",
                amount=amount,
                target_account_id=from_account_id,
                description=f"收到{from_account.name}转账"
            )
            
            self.db.add(from_transaction)
            self.db.add(to_transaction)
            self.db.commit()
            
            return True, "", transaction_id
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"转账失败: {str(e)}")
            return False, f"转账失败：{str(e)}", None
    
    def get_transactions(self, account_id: int, limit: int = 10) -> List[Transaction]:
        """获取账户交易记录"""
        return self.db.query(Transaction)\
            .filter(Transaction.account_id == account_id)\
            .order_by(Transaction.created_at.desc())\
            .limit(limit)\
            .all()
    
    def _generate_transaction_id(self) -> str:
        """生成交易编号"""
        count = self.db.query(Transaction).count()
        return f"TXN{1000 + count + 1}"

