import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm
import os

class BatchAIDetector:
    def __init__(self, model_path):
        # 明确指定使用本地文件
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path, 
            local_files_only=True  # 关键参数：只使用本地文件
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            local_files_only=True  # 关键参数：只使用本地文件
        )
        self.model.eval()
        self.label_map = {0: "人类撰写", 1: "AI生成"}

    def detect_text(self, text):
        """检测单条文本"""
        if not text or not str(text).strip():
            return {
                "ai_prob": 0.0,
                "human_prob": 0.0,
                "conclusion": "无效文本"
            }
        
        try:
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512,
                padding=True
            )
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            ai_prob = float(probs[0][1])
            human_prob = float(probs[0][0])
            
            return {
                "ai_prob": ai_prob,
                "human_prob": human_prob,
                "conclusion": self.label_map[torch.argmax(probs).item()]
            }
            
        except Exception as e:
            print(f"文本检测失败: {e}")
            return {
                "ai_prob": 0.0,
                "human_prob": 0.0,
                "conclusion": "检测失败"
            }

    def detect_batch(self, input_path, output_path, progress_callback=None):
        """批量检测CSV文件
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            progress_callback: 进度回调函数，接收当前进度(int)作为参数
        """
        try:
            # 详细记录文件处理过程
            print(f"开始处理文件: {input_path}")
            
            # 读取CSV文件，使用适当的编码处理
            df = None
            encodings = ['utf-8-sig', 'gbk', 'latin-1', 'utf-8']
            for encoding in encodings:
                try:
                    df = pd.read_csv(input_path, encoding=encoding)
                    print(f"成功使用 {encoding} 编码读取文件")
                    break
                except Exception as e:
                    print(f"使用 {encoding} 编码读取失败: {e}")
                    continue
            
            if df is None:
                print("所有编码尝试均失败")
                return False
            
            total = len(df)
            print(f"成功读取 {total} 条评论")
            print(f"文件包含列: {list(df.columns)}")
            
            # 统一列命名规范后，直接使用标准列名
            # 评论内容列统一为"评论内容"
            if '评论内容' not in df.columns:
                print("错误：CSV文件缺少'评论内容'列")
                print(f"可用列: {list(df.columns)}")
                return False
            
            content_col = '评论内容'
            print(f"使用标准列名 '{content_col}' 作为评论内容列")
            
            # 用户名列统一为"用户名"
            if '用户名' not in df.columns:
                print("错误：CSV文件缺少'用户名'列")
                print(f"可用列: {list(df.columns)}")
                return False
            
            username_col = '用户名'
            print(f"使用标准列名 '{username_col}' 作为用户名列")
            
            # 添加序号列
            df['序号'] = range(1, len(df) + 1)
            
            # 确保包含用户名列，否则添加空的用户名列
            # 列名已经统一，无需重命名
            
            # 为每条评论添加AI检测结果
            total_rows = len(df)
            for idx, row in tqdm(df.iterrows(), total=total_rows, desc="检测进度"):
                try:
                    # 检测单条评论（使用重命名后的列名）
                    comment_text = str(row['评论内容']) if pd.notna(row['评论内容']) else ""
                    result = self.detect_text(comment_text)
                    
                    # 将AI检测结果添加到数据框中
                    df.at[idx, 'ai_prob'] = result['ai_prob']
                    df.at[idx, 'human_prob'] = result['human_prob']
                    df.at[idx, 'conclusion'] = result['conclusion']
                    
                    # 调用进度回调函数
                    if progress_callback:
                        progress_callback(idx + 1)
                    
                except Exception as e:
                    print(f"处理第{idx}条评论时出错: {e}")
                    print(f"当前行数据: {row.to_dict()}")
                    df.at[idx, 'ai_prob'] = 0.0
                    df.at[idx, 'human_prob'] = 0.0
                    df.at[idx, 'conclusion'] = "处理失败"
                    
                    # 即使出错也调用进度回调
                    if progress_callback:
                        progress_callback(idx + 1)
            
            # 保存结果
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"结果已保存到: {output_path}")
            
            # 统计结果
            ai_count = len(df[df['conclusion'] == 'AI生成'])
            total_count = len(df)
            
            print(f"分析完成！AI生成比例: {ai_count/total_count:.2%}")
            return True
            
        except Exception as e:
            print(f"处理CSV文件时出错: {e}")
            import traceback
            traceback.print_exc()
            return False