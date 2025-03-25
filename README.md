# Errata - 智能题目解析系统

Errata 是一个基于通义千问2.5 VL模型的智能题目解析系统，能够自动识别和分析图片中的题目内容，并输出结构化的JSON数据。

## 功能特点

- 支持多种题型识别（选择题、填空题、解答题）
- 智能题目分割
- 自动清理选项标记
- 保留数学公式的LaTeX格式
- 结构化JSON输出

## 环境要求

- Python 3.6+
- dashscope
- python-dotenv

## 安装

1. 克隆项目到本地：
```bash
git clone [项目地址]
cd Errata
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
创建 `.env` 文件并添加以下内容：
```
DASHSCOPE_API_KEY=你的通义千问API密钥
```

## 使用方法

1. 准备待分析的题目图片

2. 修改 `main.py` 中的图片路径：
```python
image_path = "你的图片路径"
```

3. 运行程序：
```bash
python main.py
```

## 输出格式

程序将返回JSON格式的结果，包含以下字段：

```json
{
  "status": "success",
  "data": {
    "question": [
      {
        "type": "题目类型",
        "text": "题目内容",
        "options": ["选项1", "选项2", ...]  // 仅选择题包含此字段
      }
    ]
  }
}
```

## 错误处理

系统会返回详细的错误信息，包括：
- 文件不存在错误
- API调用错误
- JSON解析错误
- 环境变量配置错误

## 注意事项

- 请确保图片清晰可读
- API密钥请妥善保管，不要泄露
- 建议处理图片大小不超过10MB

## License

MIT License

## 联系方式

如有问题或建议，请提交Issue或Pull Request。