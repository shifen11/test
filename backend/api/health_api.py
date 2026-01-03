"""健康检查 API"""
from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health():
    """健康检查接口"""
    return jsonify({"status": "ok", "service": "银行智能体"})

