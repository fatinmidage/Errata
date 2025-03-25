import json
from dotenv import load_dotenv
from utils.image_analyzer import ImageAnalyzer

# 加载环境变量
load_dotenv()

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