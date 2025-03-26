import json
import os
from datetime import datetime
from dotenv import load_dotenv
from utils.image_analyzer import ImageAnalyzer

# 加载环境变量
load_dotenv()

def format_question(question, index):
    """格式化单个问题"""
    result = f"### 问题 {index}\n\n"
    result += f"**题型**：{question['type']}\n\n"
    result += f"**题目**：{question['text']}\n\n"
    result += "**选项**：\n\n"
    for i, option in enumerate(question['options'], 1):
        result += f"{chr(64+i)}. {option}\n"
    result += "\n---\n\n"
    return result

def save_to_markdown(result, image_path, output_path="analysis_result.md"):
    """将分析结果保存为格式化的markdown文件"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(output_path, "w", encoding="utf-8") as f:
        # 页眉部分
        f.write("<div align='center'>\n\n")
        f.write("# 📝 试题分析报告\n\n")
        f.write(f"*生成时间：{now}*\n\n")
        f.write("</div>\n\n")
        f.write("---\n\n")
        
        # 图片信息部分
        f.write("## 📷 图片基本信息\n\n")
        f.write("| 属性 | 内容 |\n")
        f.write("|:-----|:----|\n")
        f.write(f"| 文件名称 | `{os.path.basename(image_path)}` |\n")
        f.write(f"| 文件路径 | `{image_path}` |\n")
        f.write(f"| 处理状态 | {'✅ 成功' if result.get('status') == 'success' else '❌ 失败'} |\n\n")
        f.write("---\n\n")
        
        # 分析结果部分
        f.write("## 📋 题目详情\n\n")
        
        if 'data' in result and 'question' in result['data']:
            questions = result['data']['question']
            if isinstance(questions, list):
                for i, q in enumerate(questions, 1):
                    f.write(format_question(q, i))
        
        # 页脚
        f.write("<div align='center'>\n\n")
        f.write("---\n\n")
        f.write("*此报告由智能试题分析系统自动生成*\n\n")
        f.write("</div>")

def main():
    try:
        # 初始化分析器
        analyzer = ImageAnalyzer()
        
        # 设置图像路径
        image_path = "/Users/why/Desktop/WechatIMG877.jpg"
        
        # 分析图像
        result = analyzer.analyze_image(image_path)
        
        # 输出结果到控制台
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 保存结果到markdown文件
        save_to_markdown(result, image_path)
        print("分析结果已保存到 analysis_result.md")
        
    except Exception as e:
        print(f"程序执行出错：{str(e)}")

if __name__ == "__main__":
    main()