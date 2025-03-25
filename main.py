import os
from dashscope import MultiModalConversation

# 将xxxx/test.png替换为你本地图像的绝对路径
local_path = "/Users/why/Desktop/WechatIMG877.jpg"
image_path = f"file://{local_path}"
messages = [{
    "role": "system",
    "content": [{
        "text": """你是一个专业的题目解析器，请严格按以下规则处理图像：
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
    }]
}, {
    "role": "user",
    "content": [{
        "image": image_path
    }, {
        "text": """请按以下JSON格式输出，注意：
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
    }]
}]






response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen2.5-vl-7b-instruct',
    messages=messages)
print(response["output"]["choices"][0]["message"].content[0]["text"])