import os
from datetime import datetime
from typing import Dict, Any

# 模型配置
MODEL_CONFIG = {
    "deepseek-v3": {
        "name": "deepseek-v3",
        "display_name": "DeepSeek V3",
        "category": "search"
    },
    "deepseek-r1": {
        "name": "deepseek-r1", 
        "display_name": "DeepSeek R1",
        "category": "search"
    },
    "deepseek-v3-search": {
        "name": "deepseek-v3-search",
        "display_name": "DeepSeek V3 Search",
        "category": "search"
    },
    "deepseek-r1-search": {
        "name": "deepseek-r1-search",
        "display_name": "DeepSeek R1 Search", 
        "category": "search"
    },
    "hunyuan": {
        "name": "hunyuan",
        "display_name": "混元",
        "category": "general"
    },
    "hunyuan-t1": {
        "name": "hunyuan-t1",
        "display_name": "混元 T1",
        "category": "general"
    }
}

# 文件命名配置
FILE_NAMING_CONFIG = {
    "output_dir": "outputs",  # 输出目录
    "filename_format": "{model}_{timestamp}_{query_hash}.txt",  # 文件名格式
    "timestamp_format": "%Y%m%d_%H%M%S",  # 时间戳格式
    "max_query_length": 50,  # 查询内容最大长度（用于生成hash）
}

def get_model_config(model_name: str) -> Dict[str, Any]:
    """获取模型配置"""
    return MODEL_CONFIG.get(model_name, {
        "name": model_name,
        "display_name": model_name,
        "category": "unknown"
    })

def generate_filename(model_name: str, query: str = "", timestamp: datetime = None) -> str:
    """
    根据配置生成文件名
    
    Args:
        model_name: 模型名称
        query: 查询内容
        timestamp: 时间戳，如果为None则使用当前时间
        
    Returns:
        str: 生成的文件名
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    # 获取模型配置
    model_config = get_model_config(model_name)
    
    # 生成查询内容的hash（用于文件名）
    import hashlib
    query_hash = hashlib.md5(query.encode()).hexdigest()[:8] if query else "default"
    
    # 截断过长的查询内容
    if len(query) > FILE_NAMING_CONFIG["max_query_length"]:
        query_short = query[:FILE_NAMING_CONFIG["max_query_length"]] + "..."
    else:
        query_short = query
    
    # 生成文件名
    filename = FILE_NAMING_CONFIG["filename_format"].format(
        model=model_config["name"],
        timestamp=timestamp.strftime(FILE_NAMING_CONFIG["timestamp_format"]),
        query_hash=query_hash
    )
    
    # 确保输出目录存在
    output_dir = FILE_NAMING_CONFIG["output_dir"]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    return os.path.join(output_dir, filename)

def get_output_path(model_name: str, query: str = "") -> str:
    """
    获取输出文件路径
    
    Args:
        model_name: 模型名称
        query: 查询内容
        
    Returns:
        str: 输出文件路径
    """
    return generate_filename(model_name, query)
