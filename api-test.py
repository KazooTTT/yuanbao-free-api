import base64
import os
from dotenv import load_dotenv

import requests
from openai import OpenAI
from config import get_output_path

# 加载环境变量
load_dotenv()

base_url = "http://localhost:8002/v1/"

hy_source = "web"
# 从环境变量读取配置
hy_user = os.getenv("HY_USER")
hy_token = os.getenv("HY_TOKEN")

# 验证环境变量是否正确加载
if not hy_user or not hy_token:
    raise ValueError("请在 .env 文件中设置 HY_USER 和 HY_TOKEN")

agent_id = "naQivTmsDa"
chat_id = ""    # 可选，如果不提供会自动创建

# chat
client = OpenAI(base_url=base_url, api_key=hy_token)

# 定义查询内容
query = "请你查找今年就业率较高的专业，总结出5点。"
model_name = "deepseek-r1-search"

response = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": query}],
    stream=True,
    extra_body={
        "hy_source": hy_source,
        "hy_user": hy_user,
        "agent_id": agent_id,
        "chat_id": chat_id,
        "should_remove_conversation": False,
    },
)

# 根据配置生成输出文件路径
path = get_output_path(model_name, query)
content = ""
links = []

print(f"输出文件: {path}")

for chunk in response:
    content_piece = chunk.choices[0].delta.content or ""
    print(content_piece, end="")  # 在控制台显示
    content += content_piece
    
    # 写入原始JSON数据到文件，每个chunk后添加换行符
    with open(path, "a", encoding="utf-8") as f:
        f.write(content_piece + "\n")

print("\n\n=== 提取的正文内容 ===")
print(content)

# 可选：调用提取脚本
try:
    from extract_content import extract_content_and_links, save_extracted_content
    extracted_content, extracted_links = extract_content_and_links(path)
    save_extracted_content(extracted_content, extracted_links, "final_extracted_content.txt")
    print(f"\n=== 提取完成 ===")
    print(f"正文长度: {len(extracted_content)} 字符")
    print(f"链接数量: {len(extracted_links)} 个")
    print("结果已保存到: final_extracted_content.txt")
except ImportError:
    print("\n注意: 需要运行 extract_content.py 来提取完整内容")
