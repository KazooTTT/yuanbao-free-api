import json
import re
from typing import Dict, List, Tuple

def extract_content_and_links(file_path: str) -> Tuple[str, List[Dict]]:
    """
    从API响应文件中提取正文内容和相关链接
    
    Args:
        file_path: 输出文件路径
        
    Returns:
        Tuple[str, List[Dict]]: (正文内容, 链接列表)
    """
    content = ""
    links = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            try:
                data = json.loads(line)
                
                # 提取文本内容
                if data.get("type") == "text" and "msg" in data:
                    content += data["msg"]
                
                # 提取搜索指南中的链接
                elif data.get("type") == "searchGuid" and "docs" in data:
                    for doc in data["docs"]:
                        link_info = {
                            "title": doc.get("title", ""),
                            "url": doc.get("url", ""),
                            "source": doc.get("webSiteSource", ""),
                            "publish_time": doc.get("publish_time", ""),
                            "quote": doc.get("quote", "")[:200] + "..." if len(doc.get("quote", "")) > 200 else doc.get("quote", "")
                        }
                        links.append(link_info)
                        
            except json.JSONDecodeError:
                # 跳过非JSON行
                continue
    
    return content, links

def save_extracted_content(content: str, links: List[Dict], output_file: str = "extracted_content.txt"):
    """
    保存提取的内容到文件
    
    Args:
        content: 正文内容
        links: 链接列表
        output_file: 输出文件名
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("正文内容\n")
        f.write("=" * 50 + "\n")
        f.write(content)
        f.write("\n\n")
        
        f.write("=" * 50 + "\n")
        f.write("相关链接\n")
        f.write("=" * 50 + "\n")
        
        for i, link in enumerate(links, 1):
            f.write(f"\n{i}. {link['title']}\n")
            f.write(f"   来源: {link['source']}\n")
            f.write(f"   发布时间: {link['publish_time']}\n")
            f.write(f"   链接: {link['url']}\n")
            f.write(f"   摘要: {link['quote']}\n")
            f.write("-" * 30 + "\n")

def main():
    """主函数"""
    # 提取内容
    content, links = extract_content_and_links("output.txt")
    
    # 保存提取的内容
    save_extracted_content(content, links)
    
    print(f"提取完成！")
    print(f"正文长度: {len(content)} 字符")
    print(f"链接数量: {len(links)} 个")
    print(f"结果已保存到: extracted_content.txt")

if __name__ == "__main__":
    main()
