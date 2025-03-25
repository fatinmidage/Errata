import os
import json
import warnings
import re
from typing import List, Dict, Any
from pathlib import Path
from dashscope import MultiModalConversation
from dotenv import load_dotenv

# 忽略 urllib3 的 SSL 警告
warnings.filterwarnings('ignore', category=Warning)

# 加载环境变量
load_dotenv()

class ImageAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('DASHSCOPE_API_KEY')
        if not self.api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")
        
        self.model = 'qwen2.5-vl-7b-instruct'
    
    def _clean_json_text(self, text: str) -> str:
        """清理API返回的JSON文本，移除Markdown代码块标记"""
        # 移除开头的 ```json 和结尾的 ```
        text = re.sub(r'^```json\n', '', text)
        text = re.sub(r'\n```$', '', text)
        # 如果还有其他markdown标记，直接提取{}之间的内容
        if not text.strip().startswith('{'):
            match = re.search(r'({[\s\S]*})', text)
            if match:
                text = match.group(1)
        return text.strip()
        
    @staticmethod
    def _get_system_prompt() -> str:
        return """你是一个专业的题目解析器，请严格按以下规则处理图像：
1. 输出格式必须为严格规范的JSON，包含status和data字段
2. 当检测到多个题目时，data中的question字段应为数组
3. 题目类型识别规则：
   - 有明确选项的判定为「选择题」
   - 需填空的判定为「填空题」
   - 需完整解答的判定为「解答题」
4. 选项处理规则：
   - 清除所有选项序号标识
   - 保留选项文本内容，数学公式保持latex格式
   - 多个选项间按原始顺序排列
5. 题目分割规则：
   - 按题号分割（如"1.","2."）
   - 按空行分割（题目间距＞2倍行距）
   - 按分隔线分割"""

    @staticmethod
    def _get_user_prompt() -> str:
        return """请按以下JSON格式输出，注意：
- 若选项存在，直接输出选项内容
- 数学符号保留原始格式
- 文本中的序号自动过滤

正确格式示例：
{
  "status": "success",
  "data": {
    "question": [
      {
        "type": "选择题",
        "text": "下列运算正确的是：",
        "options": ["√2+√3=√5", "(a²)³=a⁵", "½+⅓=⅖", "2√3×3√2=6√6"]
      },
      {
        "type": "填空题",
        "text": "方程x²-5x+6=0的解是__",
        "options": []
      }
    ]
  }
}"""

    def _prepare_messages(self, image_path: str) -> List[Dict[str, Any]]:
        return [
            {
                "role": "system",
                "content": [{"text": self._get_system_prompt()}]
            },
            {
                "role": "user",
                "content": [
                    {"image": f"file://{image_path}"},
                    {"text": self._get_user_prompt()}
                ]
            }
        ]

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """分析图像并返回结构化的题目数据"""
        if not Path(image_path).exists():
            raise FileNotFoundError(f"找不到图像文件：{image_path}")

        try:
            messages = self._prepare_messages(image_path)
            response = MultiModalConversation.call(
                api_key=self.api_key,
                model=self.model,
                messages=messages
            )
            
            # 检查API响应
            if not response or "output" not in response:
                return {
                    "status": "error",
                    "message": "API 返回为空或格式错误"
                }
            
            # 获取模型输出的文本
            try:
                result_text = response["output"]["choices"][0]["message"]["content"][0]["text"]
                # 清理JSON文本
                cleaned_text = self._clean_json_text(result_text)
            except (KeyError, IndexError) as e:
                return {
                    "status": "error",
                    "message": f"API 响应格式异常: {str(e)}\n实际响应: {json.dumps(response, ensure_ascii=False)}"
                }
            
            # 尝试解析JSON
            try:
                result = json.loads(cleaned_text)
                return result
            except json.JSONDecodeError as e:
                return {
                    "status": "error",
                    "message": f"JSON解析失败: {str(e)}\n清理后的文本: {cleaned_text}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"处理失败：{str(e)}"
            }

def main():
    try:
        # 初始化分析器
        analyzer = ImageAnalyzer()
        
        # 设置图像路径
        image_path = "/Users/why/Desktop/WechatIMG877.jpg"
        
        # 分析图像
        result = analyzer.analyze_image(image_path)
        
        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"程序执行出错：{str(e)}")

if __name__ == "__main__":
    main()